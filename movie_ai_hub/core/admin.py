from django.contrib import admin
from .models import *

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "release_date", "average_rating", "box_office_revenue", "status", "popularity")
    search_fields = ("title", "keywords", "synopsis")
    list_filter = ("status", "language", "genres", "release_date")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("cast", "genres")

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "nationality", "date_of_birth")
    search_fields = ("name", "nationality")
    list_filter = ("nationality",)

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name", "nationality", "date_of_birth")
    search_fields = ("name", "nationality")

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "score", "created_at")
    list_filter = ("score",)
    search_fields = ("movie__title",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "reviewer_name", "rating", "sentiment", "sentiment_score", "created_at")
    list_filter = ("sentiment", "rating")
    search_fields = ("movie__title", "title", "text", "reviewer_name")
    readonly_fields = ("sentiment", "sentiment_score")

@admin.register(BoxOffice)
class BoxOfficeAdmin(admin.ModelAdmin):
    list_display = ("movie", "opening_weekend", "worldwide_revenue")

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "published_date")
    list_filter = ("category", "published_date")
    search_fields = ("title", "summary", "content", "tags")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Watchlist)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)
admin.site.register(AIInteraction)
