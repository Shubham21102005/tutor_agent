import asyncio
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import websockets
app = FastAPI()

load_dotenv()

DEEPGRAM_API_KEY= os.getenv("DEEPGRAM_API_KEY")

DEEPGRAM_URL = (
    "wss://api.deepgram.com/v1/listen"
    "?model=nova-3&language=en&smart_format=true"
    "&punctuate=true&interim_results=true"
    "&encoding=linear16&sample_rate=16000&channels=1"
    "&endpointing=300&utterance_end_ms=1000"
)
@app.get("/health")
def health():
    return {"status": "ok"}

@app.websocket("/ws/session/{session_id}")
async def websocket_session(websocket: WebSocket, session_id: str):
    await websocket.accept()
    print(f"websocket connected: {session_id}")
    try:
        async with websockets.connect(
            DEEPGRAM_URL,
            additional_headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}
        ) as deepgram_websocket:
            async def forward_audio():
                while True:
                    data = await websocket.receive_bytes()
                    await deepgram_websocket.send(data)
            
            async def forward_transcripts():
                accumulated = []
                async for message in deepgram_websocket:
                    data = json.loads(message)
                    message_type = data.get("type")

                    if message_type == "Results":
                        alternatives = data.get("channel", {}).get("alternatives", [{}])
                        transcript = alternatives[0].get("transcript", "")
                        is_final = data.get("is_final", False)

                        if transcript:
                            await websocket.send_json({
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
                            await websocket.send_json({
                                "type": "utterance_complete",
                                "text": full_utterance,
                            })
                            print(f"USER TURN COMPLETE: {full_utterance}")
                            accumalated = []
                            async for message in deepgram_websocket:
                                data = json.loads(message)
                                message_type = data.get(type)
                                
                                if message_type == "Results":
                                    alternatives = data.get("channel", {}).get("alternatives", [{}])
                                    transcript = alternatives[0].get("transcript","")
                                    is_final= data.get("is_final", False)
                                    if transcript:
                                        await websocket.send_json({
                                            "type": "transcript",
                                            "text": transcript,
                                            "is_final": data.get("is_final", False),
                                        })
                                    if is_final:
                                        accumalated.append(transcript)
                                elif message_type == "UtteranceEnd":
                                    if accumalated:
                                        full_utterance = " ".join(accumulated)
                                        accumalated = []
                                        await websocket.send_json({
                                            "type": "utterance_complete",
                                            "text": full_utterance,
                                        })
                                        print(f"USER TURN COMPLETE: {full_utterance}")
            await asyncio.gather(forward_audio(), forward_transcripts())


    except WebSocketDisconnect:
            print(f"session {session_id} disconnected")
    except Exception as e:
            print(f"session {session_id} error: {e}")