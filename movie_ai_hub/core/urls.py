from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import *
from . import views

router = DefaultRouter()
router.register("api/movies", MovieViewSet)
router.register("api/actors", ActorViewSet)
router.register("api/directors", DirectorViewSet)
router.register("api/genres", GenreViewSet)
router.register("api/ratings", RatingViewSet)
router.register("api/reviews", ReviewViewSet)
router.register("api/box-office", BoxOfficeViewSet)
router.register("api/articles", ArticleViewSet)

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movies, name="movies"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("actors/", views.actors, name="actors"),
    path("actors/<int:pk>/", views.actor_detail, name="actor_detail"),
    path("directors/", views.directors, name="directors"),
    path("directors/<int:pk>/", views.director_detail, name="director_detail"),
    path("genres/", views.genres, name="genres"),
    path("genres/<int:pk>/", views.genre_detail, name="genre_detail"),
    path("reviews/", views.reviews, name="reviews"),
    path("box-office/", views.box_office, name="box_office"),
    path("trending/", views.trending, name="trending"),
    path("statistics/", views.statistics, name="statistics"),
    path("recommendations/", views.recommendations, name="recommendations"),
    path("articles/", views.articles, name="articles"),
    path("articles/<slug:slug>/", views.article_detail, name="article_detail"),
    path("ai/", views.ai, name="ai"),
    path("search/", views.search, name="search"),
    path("api/ai/ask/", ai_ask, name="api_ai_ask"),
    path("api/statistics/", statistics_api, name="api_statistics"),
    path("api/trending/", trending_api, name="api_trending"),
    path("api/movies/<int:pk>/recommendations/", recommendations_api, name="api_recommendations"),
]
urlpatterns += router.urls
