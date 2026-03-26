from fastapi import APIRouter, Response, status

from app.core.config import settings
from app.models import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(service=settings.app_name, version=settings.app_version)


@router.head("", status_code=status.HTTP_200_OK)
def health_head() -> Response:
    return Response(status_code=status.HTTP_200_OK)
