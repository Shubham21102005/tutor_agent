import json
import websockets
from fastapi import WebSocket

from app.config import DEEPGRAM_API_KEY, DEEPGRAM_URL


def build_deepgram_connection():
    """Returns an unopened websockets connection context manager."""
    return websockets.connect(
        DEEPGRAM_URL,
        additional_headers={"Authorization": f"Token {DEEPGRAM_API_KEY}"},
    )


async def forward_audio(client_ws: WebSocket, deepgram_ws) -> None:
    while True:
        data = await client_ws.receive_bytes()
        await deepgram_ws.send(data)


async def forward_transcripts(client_ws: WebSocket, deepgram_ws, on_utterance_complete) -> None:
    """
    Relays interim/final transcripts to the client. Calls
    on_utterance_complete(full_text) once Deepgram signals UtteranceEnd.
    """
    accumulated = []
    async for message in deepgram_ws:
        data = json.loads(message)
        message_type = data.get("type")

        if message_type == "Results":
            alternatives = data.get("channel", {}).get("alternatives", [{}])
            transcript = alternatives[0].get("transcript", "")
            is_final = data.get("is_final", False)

            if transcript:
                await client_ws.send_json({
                    "type": "transcript",
                    "text": transcript,
                    "is_final": is_final,
                })
            if is_final:
                accumulated.append(transcript)

        elif message_type == "UtteranceEnd":
            if accumulated:
                full_utterance = " ".join(accumulated)
                accumulated = []
                await client_ws.send_json({
                    "type": "utterance_complete",
                    "text": full_utterance,
                })
                await on_utterance_complete(full_utterance)
