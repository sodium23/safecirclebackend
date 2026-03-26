from fastapi import FastAPI

from app.core.config import settings
from app.routers.health import router as health_router
from app.routers.mentor import router as mentor_router
from app.routers.training import router as training_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend APIs for SaferCircle (frontend consumed separately)",
)

app.include_router(health_router)
app.include_router(training_router)
app.include_router(mentor_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "SaferCircle backend is running"}
