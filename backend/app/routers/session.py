import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.stt import build_deepgram_connection, forward_audio, forward_transcripts
from app.services.llm import stream_llm_response
from app.state.sessions import clear_session

router = APIRouter()


@router.websocket("/ws/session/{session_id}")
async def websocket_session(websocket: WebSocket, session_id: str):
    await websocket.accept()
    print(f"websocket connected: {session_id}")

    try:
        async with build_deepgram_connection() as deepgram_ws:

            async def on_utterance_complete(text: str):
                print(f"USER TURN COMPLETE: {text}")
                await stream_llm_response(websocket, session_id, text)

            await asyncio.gather(
                forward_audio(websocket, deepgram_ws),
                forward_transcripts(websocket, deepgram_ws, on_utterance_complete),
            )

    except WebSocketDisconnect:
        print(f"session {session_id} disconnected")
        clear_session(session_id)
    except Exception as e:
        print(f"session {session_id} error: {e}")
