from fastapi import APIRouter

from app.models import DailyScenario, DailyScenarioResponseChoice, GroundMeResponse

router = APIRouter(prefix="/training", tags=["training"])


@router.get("/ground-me", response_model=GroundMeResponse)
def ground_me() -> GroundMeResponse:
    return GroundMeResponse(
        breathing_script="Inhale 4 seconds, hold 4, exhale 6. Repeat 3 times.",
        assertive_sentence="I hear you. Here's what I need going forward.",
        posture_reminder="Shoulders down, chin level, feet planted.",
        voice_tempo_reminder="Slow down by 15% and end sentences cleanly.",
    )


@router.get("/daily-scenario", response_model=DailyScenario)
def daily_scenario() -> DailyScenario:
    return DailyScenario(
        category="Workplace power dynamics",
        context="A colleague interrupts you twice in a leadership update meeting.",
        what_is_happening="Boundary testing in a visibility-heavy setting.",
        choices=[
            DailyScenarioResponseChoice(
                label="Call it out in the moment",
                short_term_effect="Raises tension quickly.",
                long_term_consequence="Can establish immediate conversational boundaries.",
            ),
            DailyScenarioResponseChoice(
                label="Reclaim calmly and continue",
                short_term_effect="Maintains room control.",
                long_term_consequence="Builds a reputation for composed authority.",
            ),
            DailyScenarioResponseChoice(
                label="Say nothing and follow up later",
                short_term_effect="Avoids immediate friction.",
                long_term_consequence="May normalize future interruptions if not addressed.",
            ),
        ],
        power_move="Use: 'I want to finish this point, then I’ll come to you.'",
    )
