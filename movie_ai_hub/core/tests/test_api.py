import pytest
from rest_framework.test import APIClient
from core.models import Movie

@pytest.mark.django_db
def test_movies_api():
    Movie.objects.create(title="API Movie", slug="api-movie", synopsis="Test", average_rating=8)
    response = APIClient().get("/api/movies/")
    assert response.status_code == 200
    assert response.data["count"] == 1

@pytest.mark.django_db
def test_ai_api_validation():
    response = APIClient().post("/api/ai/ask/", {}, format="json")
    assert response.status_code == 400
