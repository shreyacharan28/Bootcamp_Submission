import pytest
from core.models import Movie
from core.services.ai import detect_intent, ask

@pytest.mark.django_db
def test_top_rated_intent():
    assert detect_intent("What are the highest rated movies?") == "TOP_RATED_MOVIES"

@pytest.mark.django_db
def test_recommendation_intent():
    assert detect_intent("Recommend movies similar to Interstellar") == "MOVIE_RECOMMENDATION"

@pytest.mark.django_db
def test_unknown_intent():
    assert detect_intent("Tell me something random") == "UNKNOWN"

@pytest.mark.django_db
def test_ai_answer():
    Movie.objects.create(title="Test", slug="test", synopsis="Good film", average_rating=9)
    result = ask("What are the highest rated movies?")
    assert result["intent"] == "TOP_RATED_MOVIES"
    assert "Test" in result["answer"]
