from django.db.models import Q

def tokenize(value):
    return {x.strip().lower() for x in value.replace(",", " ").split() if x.strip()}

def movie_similarity(source, candidate):
    score = 0.0
    source_genres = set(source.genres.values_list("id", flat=True))
    candidate_genres = set(candidate.genres.values_list("id", flat=True))
    if source_genres and candidate_genres:
        score += 0.45 * (len(source_genres & candidate_genres) / len(source_genres | candidate_genres))
    source_cast = set(source.cast.values_list("id", flat=True))
    candidate_cast = set(candidate.cast.values_list("id", flat=True))
    if source_cast and candidate_cast:
        score += 0.25 * (len(source_cast & candidate_cast) / len(source_cast | candidate_cast))
    if source.director_id and source.director_id == candidate.director_id:
        score += 0.15
    if source.language == candidate.language:
        score += 0.05
    source_words = tokenize(source.keywords)
    candidate_words = tokenize(candidate.keywords)
    if source_words and candidate_words:
        score += 0.10 * (len(source_words & candidate_words) / len(source_words | candidate_words))
    score += min(float(candidate.average_rating) / 10, 1) * 0.05
    return round(score, 4)

def recommend_similar(movie, limit=6):
    from core.models import Movie
    candidates = Movie.objects.exclude(pk=movie.pk).prefetch_related("genres", "cast")
    ranked = sorted(candidates, key=lambda m: movie_similarity(movie, m), reverse=True)
    return [(m, movie_similarity(movie, m)) for m in ranked[:limit]]
