from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie, Actor, Director, Genre, Rating, Review, BoxOffice, Article
from .serializers import *
from .services.ai import MovieAIService
from .services.recommendations import recommend_similar
from .services.sentiment import analyze_sentiment

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().prefetch_related("genres", "cast")
    serializer_class = MovieSerializer

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        text = serializer.validated_data.get("text", "")
        label, score = analyze_sentiment(text)
        serializer.save(sentiment=label, sentiment_score=score)

class BoxOfficeViewSet(viewsets.ModelViewSet):
    queryset = BoxOffice.objects.select_related("movie")
    serializer_class = BoxOfficeSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

@api_view(["POST"])
def ai_ask(request):
    question = str(request.data.get("question", "")).strip()
    if not question:
        return Response({"success": False, "error": "Question is required."}, status=status.HTTP_400_BAD_REQUEST)
    result = MovieAIService().ask(
        question,
        request.data.get("persona", "Casual Movie Fan"),
        request.data.get("level", "Beginner"),
    )
    return Response({"success": True, **result})

@api_view(["GET"])
def statistics_api(request):
    top_rated = list(Movie.objects.order_by("-average_rating", "-vote_count")[:10].values("title", "average_rating", "vote_count"))
    top_grossing = list(Movie.objects.order_by("-box_office_revenue")[:10].values("title", "box_office_revenue"))
    trending = list(Movie.objects.order_by("-popularity")[:10].values("title", "popularity"))
    return Response({"top_rated": top_rated, "top_grossing": top_grossing, "trending": trending})

@api_view(["GET"])
def recommendations_api(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found."}, status=404)
    recs = [{"movie": MovieSerializer(m).data, "similarity": score} for m, score in recommend_similar(movie)]
    return Response(recs)

@api_view(["GET"])
def trending_api(request):
    movies = Movie.objects.order_by("-popularity")[:12]
    return Response(MovieSerializer(movies, many=True).data)
