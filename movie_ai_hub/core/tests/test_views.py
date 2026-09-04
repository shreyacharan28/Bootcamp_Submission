import pytest
from django.urls import reverse
from core.models import Movie

@pytest.mark.django_db
def test_home_page(client):
    Movie.objects.create(title="Home Movie", slug="home-movie", synopsis="Test")
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert b"Movie AI Hub" in response.content

@pytest.mark.django_db
def test_ai_page(client):
    response = client.get(reverse("ai"))
    assert response.status_code == 200
