from fastapi import APIRouter

from app.core.config import settings
from app.models import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(service=settings.app_name, version=settings.app_version)
