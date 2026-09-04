import pytest
from core.models import Movie, Genre, Director

@pytest.mark.django_db
def test_movie_creation():
    g = Genre.objects.create(name="Sci-Fi")
    d = Director.objects.create(name="Test Director")
    m = Movie.objects.create(title="Test Movie", slug="test-movie", synopsis="A test.", director=d, average_rating=8.0)
    m.genres.add(g)
    assert m.title == "Test Movie"
    assert m.genres.count() == 1

@pytest.mark.django_db
def test_movie_relationships():
    d = Director.objects.create(name="Director")
    m = Movie.objects.create(title="Movie", slug="movie", synopsis="Text", director=d)
    assert m.director.name == "Director"
