from fastapi import APIRouter

from app.models import DecisionSimulatorRequest, DecisionSimulatorResponse, MentorRequest, MentorResponse
from app.services.mentor_service import mentor_service

router = APIRouter(prefix="/mentor", tags=["mentor"])


@router.post("/coach", response_model=MentorResponse)
def coach(payload: MentorRequest) -> MentorResponse:
    return mentor_service.coach(payload)


@router.post("/decision-simulator", response_model=DecisionSimulatorResponse)
def decision_simulator(payload: DecisionSimulatorRequest) -> DecisionSimulatorResponse:
    return mentor_service.simulate_decision(payload)
