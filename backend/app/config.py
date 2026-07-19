import os
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DEEPGRAM_URL = (
    "wss://api.deepgram.com/v1/listen"
    "?model=nova-3&language=en&smart_format=true"
    "&punctuate=true&interim_results=true"
    "&encoding=linear16&sample_rate=16000&channels=1"
    "&endpointing=300&utterance_end_ms=1000"
)

LLM_MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = (
    "You are a friendly, patient AI tutor speaking with a student out loud. "
    "Keep responses conversational and reasonably concise, since they will be "
    "spoken aloud via text-to-speech. Avoid long lists or heavy formatting. "
    "Explain concepts clearly, check understanding, and encourage questions."
)
