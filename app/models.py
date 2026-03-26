from typing import Literal
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str
    version: str


class GroundMeResponse(BaseModel):
    breathing_script: str
    assertive_sentence: str
    posture_reminder: str
    voice_tempo_reminder: str


class DailyScenarioResponseChoice(BaseModel):
    label: str
    short_term_effect: str
    long_term_consequence: str


class DailyScenario(BaseModel):
    category: str
    context: str
    what_is_happening: str
    choices: list[DailyScenarioResponseChoice]
    power_move: str


class DecisionSimulatorRequest(BaseModel):
    situation_summary: str = Field(min_length=10, max_length=1500)
    planned_action: str = Field(min_length=5, max_length=500)


class DecisionOption(BaseModel):
    title: str
    emotional_impact: str
    reputational_impact: str
    long_term_effect: str


class DecisionSimulatorResponse(BaseModel):
    option_a_immediate_action: DecisionOption
    option_b_strategic_alternative: DecisionOption
    option_c_delay_or_silence: DecisionOption
    strategic_recommendation: str


class MentorRequest(BaseModel):
    category: str = Field(min_length=3, max_length=120)
    user_context: str = Field(min_length=10, max_length=2000)


class MentorResponse(BaseModel):
    emotional_grounding: str
    pattern_recall: str
    strategic_framing: str
    clear_choices: list[str]
    long_term_consequence: str
