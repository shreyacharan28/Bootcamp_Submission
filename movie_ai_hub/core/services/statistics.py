from django.db.models import Avg, Count, Sum

def dashboard_stats():
    from core.models import Movie, Actor, Director, Genre, Review
    return {
        "movies": Movie.objects.count(),
        "actors": Actor.objects.count(),
        "directors": Director.objects.count(),
        "genres": Genre.objects.count(),
        "reviews": Review.objects.count(),
        "average_rating": round(float(Movie.objects.aggregate(v=Avg("average_rating"))["v"] or 0), 1),
        "top_rated": Movie.objects.order_by("-average_rating", "-vote_count").first(),
        "top_grossing": Movie.objects.order_by("-box_office_revenue").first(),
        "top_genre": Genre.objects.annotate(n=Count("movies")).order_by("-n").first(),
    }

def analytics():
    from core.models import Movie
    return {
        "top_rated": list(Movie.objects.order_by("-average_rating", "-vote_count")[:10]),
        "top_grossing": list(Movie.objects.order_by("-box_office_revenue")[:10]),
        "popular": list(Movie.objects.order_by("-popularity")[:10]),
    }
