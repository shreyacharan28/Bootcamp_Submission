from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=160)
    biography = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    profile_image = models.URLField(blank=True)
    awards = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=160)
    biography = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    profile_image = models.URLField(blank=True)
    awards = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


class Movie(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"), ("released", "Released"),
        ("theatres", "In Theatres"), ("streaming", "Streaming"),
        ("archived", "Archived"),
    ]
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    poster = models.URLField(blank=True)
    backdrop = models.URLField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.PositiveIntegerField(default=120, help_text="Runtime in minutes")
    language = models.CharField(max_length=80, default="English")
    country = models.CharField(max_length=120, blank=True)
    synopsis = models.TextField()
    certification = models.CharField(max_length=20, blank=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    box_office_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    vote_count = models.PositiveIntegerField(default=0)
    trailer_url = models.URLField(blank=True)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, blank=True, related_name="movies")
    cast = models.ManyToManyField(Actor, blank=True, related_name="movies")
    genres = models.ManyToManyField(Genre, blank=True, related_name="movies")
    keywords = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="released")
    popularity = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-popularity", "-average_rating", "title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["release_date"]),
            models.Index(fields=["average_rating"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.title


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["movie", "user"], name="unique_user_movie_rating")
        ]

    def __str__(self):
        return f"{self.movie.title}: {self.score}"


class Review(models.Model):
    SENTIMENT_CHOICES = [("positive", "Positive"), ("neutral", "Neutral"), ("negative", "Negative")]
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    reviewer_name = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=220)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    helpful_count = models.PositiveIntegerField(default=0)
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default="neutral")
    sentiment_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["sentiment"]), models.Index(fields=["movie", "rating"])]

    def __str__(self):
        return f"{self.movie.title} - {self.title}"


class BoxOffice(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name="box_office")
    opening_weekend = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    domestic_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    international_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    worldwide_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    @property
    def estimated_profit(self):
        return self.worldwide_revenue - self.movie.budget

    def __str__(self):
        return f"Box office - {self.movie.title}"


class Article(models.Model):
    CATEGORY_CHOICES = [
        ("movies", "Movies"), ("actors", "Actors"), ("directors", "Directors"),
        ("reviews", "Reviews"), ("analysis", "Analysis"), ("box_office", "Box Office"),
        ("industry", "Industry"), ("ai", "AI & Entertainment"), ("news", "News"),
    ]
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    content = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="movies")
    author = models.CharField(max_length=120, default="Movie AI Editorial")
    image = models.URLField(blank=True)
    published_date = models.DateField(auto_now_add=True)
    source_url = models.URLField(blank=True)
    tags = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "movie"], name="unique_watchlist_movie")]


class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, default="New Movie Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChatMessage(models.Model):
    ROLE_CHOICES = [("user", "User"), ("assistant", "Assistant")]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class AIInteraction(models.Model):
    question = models.TextField()
    intent = models.CharField(max_length=80)
    persona = models.CharField(max_length=80, default="Casual Movie Fan")
    level = models.CharField(max_length=30, default="Beginner")
    source = models.CharField(max_length=120, default="local")
    created_at = models.DateTimeField(auto_now_add=True)
