from fastapi import WebSocket
from groq import Groq

from app.config import GROQ_API_KEY, LLM_MODEL, SYSTEM_PROMPT
from app.state.sessions import get_history, append_message

groq_client = Groq(api_key=GROQ_API_KEY)


async def stream_llm_response(websocket: WebSocket, session_id: str, user_text: str) -> None:
    append_message(session_id, "user", user_text)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history(session_id)

    await websocket.send_json({"type": "llm_start"})

    full_reply = ""
    stream = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            full_reply += delta
            await websocket.send_json({"type": "llm_token", "text": delta})

    append_message(session_id, "assistant", full_reply)
    await websocket.send_json({"type": "llm_end", "text": full_reply})
