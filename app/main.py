from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SafeCircle backend is ready to accept requests.")
    yield
    logger.info("SafeCircle backend is shutting down.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://safecircle1.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# HEALTH CHECK (DO NOT TOUCH)
# -------------------------
@app.get("/")
def home():
    return {"status": "alive"}

@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# SAFE GEMINI SETUP
# -------------------------
def get_model():
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("Missing GEMINI_API_KEY")

    genai.configure(api_key=api_key)

    return genai.GenerativeModel("gemini-2.5-flash")


# -------------------------
# CHAT ENDPOINT
# -------------------------
@app.get("/chat")
def chat(message: str):
    try:
        model = get_model()  # initialized ONLY when needed
        response = model.generate_content(message)
        return {"reply": response.text}
    except Exception as e:
        return {
            "reply": "AI temporarily unavailable. Stay in a safe place.",
            "error": str(e),
            "degraded": True
        }

@app.get("/scenario/today")
def scenario():
    return {
        "situation": "A stranger is following you late at night.",
        "choices": [
            {"id": "a", "text": "Ignore and keep walking"},
            {"id": "b", "text": "Enter a nearby shop"},
        ],
        "outcomes": {
            "a": "Risk increases as isolation continues.",
            "b": "You move into a safer public space."
        },
        "power_move": "Always move toward visibility and people."
    }
