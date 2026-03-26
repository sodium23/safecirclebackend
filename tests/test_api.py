from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_ground_me() -> None:
    response = client.get('/training/ground-me')
    assert response.status_code == 200
    body = response.json()
    assert 'breathing_script' in body
    assert 'assertive_sentence' in body


def test_mentor_coach_fallback() -> None:
    payload = {
        'category': 'Workplace power dynamics',
        'user_context': 'My manager dismisses my ideas in meetings and I freeze.',
    }
    response = client.post('/mentor/coach', json=payload)
    assert response.status_code == 200
    assert 'strategic_framing' in response.json()
