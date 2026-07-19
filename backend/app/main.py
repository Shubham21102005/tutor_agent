from fastapi import FastAPI

from app.routers.session import router as session_router

app = FastAPI()
app.include_router(session_router)


@app.get("/health")
def health():
    return {"status": "ok"}
