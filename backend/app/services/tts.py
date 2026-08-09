import httpx
from app.config import DEEPGRAM_API_KEY, TTS_URL


async def synthesize_speech(text: str) -> bytes:
    """Sends text to Deepgram Aura-2, returns raw 16-bit PCM audio bytes."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TTS_URL,
            headers={
                "Authorization": f"Token {DEEPGRAM_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"text": text},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.content