from django.shortcuts import get_object_or_404, render
from django.db.models import Q, Avg
from .models import Movie, Actor, Director, Genre, Review, BoxOffice, Article
from .services.statistics import dashboard_stats, analytics
from .services.search import global_search
from .services.recommendations import recommend_similar
from .services.ai import MovieAIService

def home(request):
    return render(request, "index.html", {
        "stats": dashboard_stats(),
        "trending": Movie.objects.order_by("-popularity")[:6],
        "top_rated": Movie.objects.order_by("-average_rating")[:6],
    })

def movies(request):
    qs = Movie.objects.all()
    q = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "")
    year = request.GET.get("year", "")
    min_rating = request.GET.get("min_rating", "")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(keywords__icontains=q) | Q(synopsis__icontains=q))
    if genre:
        qs = qs.filter(genres__id=genre)
    if year:
        qs = qs.filter(release_date__year=year)
    if min_rating:
        qs = qs.filter(average_rating__gte=min_rating)
    return render(request, "movies/list.html", {"movies": qs.distinct(), "genres": Genre.objects.all(), "query": q})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.prefetch_related("genres", "cast"), pk=pk)
    return render(request, "movies/detail.html", {"movie": movie, "recommendations": recommend_similar(movie, 6),
        "reviews": movie.reviews.all()[:8]})

def actors(request):
    q = request.GET.get("q", "")
    qs = Actor.objects.filter(name__icontains=q) if q else Actor.objects.all()
    return render(request, "people/list.html", {"items": qs, "kind": "Actors", "detail_url": "actor_detail"})

def actor_detail(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    return render(request, "people/detail.html", {"person": actor, "movies": actor.movies.all(), "kind": "Actor"})

def directors(request):
    q = request.GET.get("q", "")
    qs = Director.objects.filter(name__icontains=q) if q else Director.objects.all()
    return render(request, "people/list.html", {"items": qs, "kind": "Directors", "detail_url": "director_detail"})

def director_detail(request, pk):
    director = get_object_or_404(Director, pk=pk)
    return render(request, "people/detail.html", {"person": director, "movies": director.movies.all(), "kind": "Director"})

def genres(request):
    return render(request, "genres/list.html", {"genres": Genre.objects.all()})

def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    return render(request, "genres/detail.html", {"genre": genre, "movies": genre.movies.all()})

def reviews(request):
    return render(request, "reviews/list.html", {"reviews": Review.objects.select_related("movie")[:100]})

def box_office(request):
    return render(request, "box_office.html", {"movies": Movie.objects.order_by("-box_office_revenue")[:30]})

def trending(request):
    return render(request, "trending.html", {"movies": Movie.objects.order_by("-popularity")[:20]})

def statistics(request):
    return render(request, "statistics.html", analytics())

def recommendations(request):
    return render(request, "recommendations.html", {"movies": Movie.objects.order_by("-average_rating")[:12]})

def articles(request):
    return render(request, "articles/list.html", {"articles": Article.objects.all()})

def article_detail(request, slug):
    return render(request, "articles/detail.html", {"article": get_object_or_404(Article, slug=slug)})

def ai(request):
    result = None
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            result = MovieAIService().ask(question, request.POST.get("persona", "Casual Movie Fan"), request.POST.get("level", "Beginner"))
    return render(request, "ai.html", {"result": result})

def search(request):
    query = request.GET.get("q", "")
    return render(request, "search.html", {"query": query, "results": global_search(query)})
