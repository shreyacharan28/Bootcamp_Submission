"""
AI Movie Assistant service.

`ask()` / `MovieAIService.ask()` is the single entry point used by both the
plain server-rendered `/ai/` page (core.views.ai) and the JSON API
(`/api/ai/ask/`, core.api_views.ai_ask). It is deliberately defensive: intent
detection now looks for real actors/directors/genres/movies mentioned by
name -- not just trigger words like "actor" or "genre" -- and the whole
thing is wrapped so a lookup problem degrades to a helpful message instead
of a hard 500, which is what made it look like "the AI isn't answering".
"""
import logging

from core.models import Actor, Director, Genre, Movie
from core.services.recommendations import recommend_similar
from core.services.statistics import analytics

logger = logging.getLogger(__name__)

# Keyword phrases used to detect intent. Matching is done against a
# normalized copy of the question (lowercased, hyphens turned into spaces),
# so phrasing like "highest-rated" and "highest rated" are both recognised.
INTENTS = {
    "TOP_RATED_MOVIES": ["highest rated", "top rated", "best rated", "best movies"],
    "TOP_BOX_OFFICE": ["box office", "highest grossing", "most revenue"],
    "TRENDING_MOVIES": ["trending", "popular movies", "popular films"],
    "MOVIE_RECOMMENDATION": ["recommend", "similar to", "what should i watch", "suggest movies", "suggest a movie"],
    "MOVIE_COMPARISON": ["compare", "versus", " vs ", " vs."],
    "ACTOR_INFO": ["actor", "actress", "cast", "filmography", "starring", "who stars"],
    "DIRECTOR_INFO": ["director", "directed", "who directed"],
    "GENRE_INFO": ["genre"],
    "MOVIE_INFO": ["movie", "film", "rating", "runtime", "released"],
}


def _normalize(question):
    return f" {question.lower().replace('-', ' ')} "


def _matches_any(normalized_question, phrases):
    return any(phrase in normalized_question for phrase in phrases)


def _mentions_any_name(question, names):
    """True if any of the given names appears as a substring of the question."""
    q = question.lower()
    return any(name.lower() in q for name in names if name)


def find_movie_from_text(question):
    q = question.lower()
    for m in Movie.objects.all():
        if m.title.lower() in q:
            return m
    return None


def find_person(question, model):
    q = question.lower()
    for obj in model.objects.all():
        if obj.name.lower() in q:
            return obj
    return None


def find_genre(question):
    q = question.lower()
    for genre in Genre.objects.all():
        if genre.name.lower() in q:
            return genre
    return None


def format_movies(movies):
    return [f"{m.title} ({m.average_rating}/10)" for m in movies]


def compare_movies(question):
    found = [m for m in Movie.objects.all() if m.title.lower() in question.lower()]
    if len(found) < 2:
        return "Please mention the titles of two movies that you want me to compare."
    a, b = found[:2]
    return (f"{a.title}: rating {a.average_rating}/10, revenue {a.box_office_revenue:,.0f}, "
            f"runtime {a.runtime} min.\n{b.title}: rating {b.average_rating}/10, "
            f"revenue {b.box_office_revenue:,.0f}, runtime {b.runtime} min.")


def detect_intent(question):
    """
    Decide what the user is asking about.

    Order of priority: an explicit comparison or recommendation request
    wins first (those keywords are unambiguous); then the "top N" style
    lists; then, importantly, a *named* actor/director/genre/movie
    mentioned anywhere in the question -- this is what makes questions
    like "Show movies with Tom Hanks" resolve to ACTOR_INFO instead of
    falling through to the generic MOVIE_INFO bucket just because the
    word "movies" is in there too. Keyword-only fallbacks run last, for
    questions that name the category but not a specific entity.
    """
    q_norm = _normalize(question)

    if _matches_any(q_norm, INTENTS["MOVIE_COMPARISON"]):
        return "MOVIE_COMPARISON"
    if _matches_any(q_norm, INTENTS["MOVIE_RECOMMENDATION"]):
        return "MOVIE_RECOMMENDATION"
    if _matches_any(q_norm, INTENTS["TOP_BOX_OFFICE"]):
        return "TOP_BOX_OFFICE"
    if _matches_any(q_norm, INTENTS["TRENDING_MOVIES"]):
        return "TRENDING_MOVIES"
    if _matches_any(q_norm, INTENTS["TOP_RATED_MOVIES"]):
        return "TOP_RATED_MOVIES"

    # Named-entity checks (run before the generic keyword fallbacks below).
    if _matches_any(q_norm, INTENTS["ACTOR_INFO"]) or find_person(question, Actor):
        return "ACTOR_INFO"
    if _matches_any(q_norm, INTENTS["DIRECTOR_INFO"]) or find_person(question, Director):
        return "DIRECTOR_INFO"
    if _matches_any(q_norm, INTENTS["GENRE_INFO"]) or find_genre(question):
        return "GENRE_INFO"
    if _matches_any(q_norm, INTENTS["MOVIE_INFO"]) or find_movie_from_text(question):
        return "MOVIE_INFO"

    return "UNKNOWN"


def _answer_for(intent, question):
    if intent == "TOP_RATED_MOVIES":
        movies = analytics()["top_rated"][:5]
        if not movies:
            return "There's no movie data loaded yet. Run `python manage.py seed_data` first."
        return "Top-rated movies:\n" + "\n".join(f"• {x}" for x in format_movies(movies))

    if intent == "TOP_BOX_OFFICE":
        movies = analytics()["top_grossing"][:5]
        if not movies:
            return "There's no movie data loaded yet. Run `python manage.py seed_data` first."
        return "Highest-grossing movies:\n" + "\n".join(
            f"• {x.title} — {x.box_office_revenue:,.0f}" for x in movies)

    if intent == "TRENDING_MOVIES":
        movies = analytics()["popular"][:5]
        if not movies:
            return "There's no movie data loaded yet. Run `python manage.py seed_data` first."
        return "Trending right now in the demo dataset:\n" + "\n".join(f"• {x.title}" for x in movies)

    if intent == "MOVIE_RECOMMENDATION":
        movie = find_movie_from_text(question)
        if not movie:
            return "Tell me a movie you liked and I’ll find similar titles from the catalog."
        recs = recommend_similar(movie, 5)
        if not recs:
            return f"I couldn't find anything similar to {movie.title} in the catalog yet."
        return f"If you liked {movie.title}, try:\n" + "\n".join(
            f"• {m.title} — similarity {score:.0%}" for m, score in recs)

    if intent == "MOVIE_COMPARISON":
        return compare_movies(question)

    if intent == "ACTOR_INFO":
        actor = find_person(question, Actor)
        if not actor:
            return "Mention an actor's name and I’ll show their filmography and movie statistics."
        titles = actor.movies.order_by("-average_rating")[:5]
        films = ", ".join(x.title for x in titles) or "No movies on file for them yet."
        return f"{actor.name}: {actor.biography or 'Profile available in the database.'}\nTop films: {films}"

    if intent == "DIRECTOR_INFO":
        director = find_person(question, Director)
        if not director:
            return "Mention a director's name and I’ll show their filmography and statistics."
        titles = director.movies.order_by("-average_rating")[:5]
        films = ", ".join(x.title for x in titles) or "No movies on file for them yet."
        return f"{director.name}: {director.biography or 'Profile available in the database.'}\nTop films: {films}"

    if intent == "GENRE_INFO":
        genre = find_genre(question)
        if not genre:
            names = ", ".join(Genre.objects.values_list("name", flat=True)) or "Action, Drama, Comedy..."
            return f"Mention a genre such as {names}."
        movies = genre.movies.order_by("-average_rating")[:5]
        titles = ", ".join(x.title for x in movies) or "no titles catalogued yet"
        return f"{genre.name}: {genre.movies.count()} movies. Top titles: {titles}"

    if intent == "MOVIE_INFO":
        movie = find_movie_from_text(question)
        if not movie:
            return "Mention a movie title and I’ll retrieve its details."
        return (f"{movie.title}: {movie.synopsis} Rating: {movie.average_rating}/10. "
                f"Runtime: {movie.runtime} min.")

    return ("I can help with movie discovery, ratings, box office, actors, directors, "
            "genres, comparisons, recommendations, and statistics. Try naming a movie, "
            "actor, or director, or ask things like 'What are the highest rated movies?'.")


def ask(question, persona="Casual Movie Fan", level="Beginner"):
    """
    Answer a natural-language question about the movie catalog.

    Wrapped in a broad except so that any unexpected error (bad data, a
    lookup bug, etc.) turns into a normal, apologetic answer instead of an
    unhandled exception -- the calling views never need their own
    try/except to keep the page from crashing.
    """
    intent = "UNKNOWN"
    try:
        intent = detect_intent(question)
        answer = _answer_for(intent, question)
    except Exception:  # noqa: BLE001 -- last-resort safety net
        logger.exception("MovieAIService.ask failed for question=%r", question)
        answer = ("Sorry, I ran into a problem answering that. Please try rephrasing, "
                  "or ask about a specific movie, actor, director, or genre.")
    return {"intent": intent, "answer": answer, "persona": persona, "level": level, "source": "local_database"}


class MovieAIService:
    def ask(self, question, persona=None, level=None):
        return ask(question, persona or "Casual Movie Fan", level or "Beginner")
