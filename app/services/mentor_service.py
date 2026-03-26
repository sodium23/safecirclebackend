import json
from typing import Any

from app.core.config import settings
from app.models import DecisionSimulatorRequest, DecisionSimulatorResponse, MentorRequest, MentorResponse

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None


TOUGH_OLDER_SISTER_SYSTEM_PROMPT = """
You are SaferCircle, a tough older sister mentor.

Always respond in a style that is:
- direct
- protective
- strategic
- emotionally intelligent
- not dramatic
- not reckless

Safety and ethics rules:
- no hate-based framing
- no encouragement of violence or retaliation
- no clinical diagnosis
- no legal claims unless explicitly uncertain and framed as non-legal advice

Response structure:
1) emotional grounding
2) pattern recall
3) strategic framing
4) clear choices
5) long-term consequences
""".strip()


class MentorService:
    def __init__(self) -> None:
        self._enabled = bool(settings.gemini_api_key and genai)
        self._model = None
        if self._enabled:
            genai.configure(api_key=settings.gemini_api_key)
            self._model = genai.GenerativeModel(settings.gemini_model)

    @property
    def enabled(self) -> bool:
        return self._enabled

    def coach(self, payload: MentorRequest) -> MentorResponse:
        if not self._enabled:
            return MentorResponse(
                emotional_grounding="Take one breath. You're not weak; you're gathering control.",
                pattern_recall="You reported similar pressure moments before. The pattern is push, then your self-doubt.",
                strategic_framing="This is not about being liked right now. It's about setting the terms of respect.",
                clear_choices=[
                    "State your boundary in one sentence and pause.",
                    "Ask one clarifying question to force accountability.",
                    "Exit politely and revisit with a written response.",
                ],
                long_term_consequence="Every clear boundary you enforce trains people how to treat you next time.",
            )

        prompt = (
            f"{TOUGH_OLDER_SISTER_SYSTEM_PROMPT}\n\n"
            "Return JSON with keys: emotional_grounding, pattern_recall, strategic_framing, clear_choices, long_term_consequence.\n"
            f"Category: {payload.category}\n"
            f"User context: {payload.user_context}\n"
        )
        response = self._model.generate_content(prompt)
        return _parse_json_response(response.text, MentorResponse)

    def simulate_decision(self, payload: DecisionSimulatorRequest) -> DecisionSimulatorResponse:
        if not self._enabled:
            return DecisionSimulatorResponse(
                option_a_immediate_action={
                    "title": "Send it now",
                    "emotional_impact": "Immediate relief, but likely anxiety rebound.",
                    "reputational_impact": "May look reactive if tone is emotional.",
                    "long_term_effect": "Can reduce leverage if you reveal your full position too early.",
                },
                option_b_strategic_alternative={
                    "title": "Refine and send a concise boundary statement",
                    "emotional_impact": "Less emotional discharge, more control.",
                    "reputational_impact": "Signals composure and standards.",
                    "long_term_effect": "Builds a repeatable pattern of calm authority.",
                },
                option_c_delay_or_silence={
                    "title": "Pause 24 hours",
                    "emotional_impact": "Discomfort now, clarity later.",
                    "reputational_impact": "Can increase perceived discipline.",
                    "long_term_effect": "Useful when the other side benefits from your impulse.",
                },
                strategic_recommendation="Default to Option B unless timing risk is critical. Control first, expression second.",
            )

        prompt = (
            f"{TOUGH_OLDER_SISTER_SYSTEM_PROMPT}\n\n"
            "Return JSON with keys: option_a_immediate_action, option_b_strategic_alternative, option_c_delay_or_silence, strategic_recommendation.\n"
            "Each option must contain: title, emotional_impact, reputational_impact, long_term_effect.\n"
            f"Situation summary: {payload.situation_summary}\n"
            f"Planned action: {payload.planned_action}\n"
        )
        response = self._model.generate_content(prompt)
        return _parse_json_response(response.text, DecisionSimulatorResponse)


mentor_service = MentorService()


def _parse_json_response(raw: str, schema: Any) -> Any:
    cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
    data = json.loads(cleaned)
    return schema.model_validate(data)
