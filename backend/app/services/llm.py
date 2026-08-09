import re
from fastapi import WebSocket
from groq import Groq
import json
from app.config import GROQ_API_KEY, LLM_MODEL, SYSTEM_PROMPT
from app.state.sessions import get_history, append_message, append_raw
from app.services.tts import synthesize_speech
from app.tools.whiteboard_tools import WHITEBOARD_TOOLS

groq_client = Groq(api_key=GROQ_API_KEY)

_SENTENCE_END = re.compile(r'(?<=[.!?])\s+')
MAX_TOOL_TURNS=5

def _extract_complete_sentences(buffer: str) -> tuple[list[str], str]:
    """Splits buffer into finished sentences plus a leftover remainder."""
    parts = _SENTENCE_END.split(buffer)
    if len(parts) <= 1:
        return [], buffer
    return parts[:-1], parts[-1]

async def _speak_and_send(websocket: WebSocket, sentence: str) -> None:
    if sentence.strip():
        audio_bytes = await synthesize_speech(sentence)
        await websocket.send_bytes(audio_bytes)


async def stream_llm_response(websocket: WebSocket, session_id: str, user_text: str) -> None:
    append_message(session_id, "user", user_text)
    await websocket.send_json({"type": "llm_start"})

    full_reply_for_history = ""

    for _ in range(MAX_TOOL_TURNS):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history(session_id)
        sentence_buffer = ""
        turn_text = ""
        tool_call_builders = {}
        finish_reason = None

        stream = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            tools=WHITEBOARD_TOOLS,
            tool_choice="auto",
            stream=True,
        )

        for chunk in stream:
            choice = chunk.choices[0]
            delta = choice.delta

            if delta.content:
                turn_text += delta.content
                sentence_buffer += delta.content
                await websocket.send_json({"type": "llm_token", "text": delta.content})

                complete_sentences, sentence_buffer = _extract_complete_sentences(sentence_buffer)
                for sentence in complete_sentences:
                    await _speak_and_send(websocket, sentence)

            if delta.tool_calls:
                for tc_delta in delta.tool_calls:
                    idx = tc_delta.index
                    builder = tool_call_builders.setdefault(idx, {"id": None, "name": None, "arguments": ""})
                    if tc_delta.id:
                        builder["id"] = tc_delta.id
                    if tc_delta.function:
                        if tc_delta.function.name:
                            builder["name"] = tc_delta.function.name
                        if tc_delta.function.arguments:
                            builder["arguments"] += tc_delta.function.arguments

            if choice.finish_reason:
                finish_reason = choice.finish_reason

        await _speak_and_send(websocket, sentence_buffer)  # flush trailing partial sentence
        full_reply_for_history += turn_text

        if finish_reason == "tool_calls" and tool_call_builders:
            tool_calls_payload = [
                {
                    "id": b["id"],
                    "type": "function",
                    "function": {"name": b["name"], "arguments": b["arguments"]},
                }
                for b in tool_call_builders.values()
            ]

            append_raw(session_id, {
                "role": "assistant",
                "content": turn_text or None,
                "tool_calls": tool_calls_payload,
            })

            for builder in tool_call_builders.values():
                try:
                    args = json.loads(builder["arguments"]) if builder["arguments"] else {}
                except json.JSONDecodeError:
                    args = {}

                await websocket.send_json({
                    "type": "whiteboard_action",
                    "action": builder["name"],
                    "payload": args,
                })

                append_raw(session_id, {
                    "role": "tool",
                    "tool_call_id": builder["id"],
                    "content": "Done.",
                })

            continue  # let the model keep talking after the tool result

        append_message(session_id, "assistant", turn_text)
        break

    await websocket.send_json({"type": "llm_end", "text": full_reply_for_history})