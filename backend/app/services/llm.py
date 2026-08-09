import re
from fastapi import WebSocket
from groq import Groq

from app.config import GROQ_API_KEY, LLM_MODEL, SYSTEM_PROMPT
from app.state.sessions import get_history, append_message
from app.services.tts import synthesize_speech

groq_client = Groq(api_key=GROQ_API_KEY)

_SENTENCE_END = re.compile(r'(?<=[.!?])\s+')


def _extract_complete_sentences(buffer: str) -> tuple[list[str], str]:
    """Splits buffer into finished sentences plus a leftover remainder."""
    parts = _SENTENCE_END.split(buffer)
    if len(parts) <= 1:
        return [], buffer
    return parts[:-1], parts[-1]


async def stream_llm_response(websocket: WebSocket, session_id: str, user_text: str) -> None:
    append_message(session_id, "user", user_text)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history(session_id)

    await websocket.send_json({"type": "llm_start"})

    full_reply = ""
    sentence_buffer = ""

    stream = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if not delta:
            continue

        full_reply += delta
        sentence_buffer += delta
        await websocket.send_json({"type": "llm_token", "text": delta})

        complete_sentences, sentence_buffer = _extract_complete_sentences(sentence_buffer)
        for sentence in complete_sentences:
            if sentence.strip():
                audio_bytes = await synthesize_speech(sentence)
                await websocket.send_bytes(audio_bytes)

    if sentence_buffer.strip():
        audio_bytes = await synthesize_speech(sentence_buffer)
        await websocket.send_bytes(audio_bytes)

    append_message(session_id, "assistant", full_reply)
    await websocket.send_json({"type": "llm_end", "text": full_reply})