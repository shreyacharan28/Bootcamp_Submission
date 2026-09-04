from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import MinValueValidator, MaxValueValidator

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Actor", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=160)), ("biography", models.TextField(blank=True)),
            ("date_of_birth", models.DateField(blank=True, null=True)), ("nationality", models.CharField(blank=True, max_length=100)),
            ("profile_image", models.URLField(blank=True)), ("awards", models.TextField(blank=True)),
        ]),
        migrations.CreateModel(name="Director", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=160)), ("biography", models.TextField(blank=True)),
            ("date_of_birth", models.DateField(blank=True, null=True)), ("nationality", models.CharField(blank=True, max_length=100)),
            ("profile_image", models.URLField(blank=True)), ("awards", models.TextField(blank=True)),
        ]),
        migrations.CreateModel(name="Genre", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=80, unique=True)), ("description", models.TextField(blank=True)),
        ]),
        migrations.CreateModel(name="Movie", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=220)), ("slug", models.SlugField(unique=True)),
            ("poster", models.URLField(blank=True)), ("backdrop", models.URLField(blank=True)),
            ("release_date", models.DateField(blank=True, null=True)), ("runtime", models.PositiveIntegerField(default=120)),
            ("language", models.CharField(default="English", max_length=80)), ("country", models.CharField(blank=True, max_length=120)),
            ("synopsis", models.TextField()), ("certification", models.CharField(blank=True, max_length=20)),
            ("budget", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ("box_office_revenue", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ("average_rating", models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[MinValueValidator(0), MaxValueValidator(10)])),
            ("vote_count", models.PositiveIntegerField(default=0)), ("trailer_url", models.URLField(blank=True)),
            ("keywords", models.CharField(blank=True, max_length=500)), ("status", models.CharField(choices=[("upcoming","Upcoming"),("released","Released"),("theatres","In Theatres"),("streaming","Streaming"),("archived","Archived")], default="released", max_length=20)),
            ("popularity", models.FloatField(default=0)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("director", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="movies", to="core.director")),
            ("cast", models.ManyToManyField(blank=True, related_name="movies", to="core.actor")),
            ("genres", models.ManyToManyField(blank=True, related_name="movies", to="core.genre")),
        ]),
        migrations.CreateModel(name="Rating", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("score", models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ratings", to="core.movie")),
            ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="Review", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("reviewer_name", models.CharField(blank=True, max_length=120)), ("title", models.CharField(max_length=220)),
            ("text", models.TextField()), ("rating", models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])),
            ("helpful_count", models.PositiveIntegerField(default=0)), ("sentiment", models.CharField(choices=[("positive","Positive"),("neutral","Neutral"),("negative","Negative")], default="neutral", max_length=20)),
            ("sentiment_score", models.FloatField(default=0)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="core.movie")),
            ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="BoxOffice", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("opening_weekend", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ("domestic_revenue", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ("international_revenue", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ("worldwide_revenue", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ("movie", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="box_office", to="core.movie")),
        ]),
        migrations.CreateModel(name="Article", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=220)), ("slug", models.SlugField(unique=True)), ("summary", models.TextField()),
            ("content", models.TextField()), ("category", models.CharField(choices=[("movies","Movies"),("actors","Actors"),("directors","Directors"),("reviews","Reviews"),("analysis","Analysis"),("box_office","Box Office"),("industry","Industry"),("ai","AI & Entertainment"),("news","News")], default="movies", max_length=30)),
            ("author", models.CharField(default="Movie AI Editorial", max_length=120)), ("image", models.URLField(blank=True)),
            ("published_date", models.DateField(auto_now_add=True)), ("source_url", models.URLField(blank=True)), ("tags", models.CharField(blank=True, max_length=300)),
        ]),
        migrations.CreateModel(name="Watchlist", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.movie")),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="ChatSession", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(default="New Movie Chat", max_length=200)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="ChatMessage", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("role", models.CharField(choices=[("user","User"),("assistant","Assistant")], max_length=20)), ("content", models.TextField()), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("session", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="core.chatsession")),
        ]),
        migrations.CreateModel(name="AIInteraction", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("question", models.TextField()), ("intent", models.CharField(max_length=80)), ("persona", models.CharField(default="Casual Movie Fan", max_length=80)),
            ("level", models.CharField(default="Beginner", max_length=30)), ("source", models.CharField(default="local", max_length=120)), ("created_at", models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.AddConstraint(model_name="rating", constraint=models.UniqueConstraint(fields=("movie","user"), name="unique_user_movie_rating")),
        migrations.AddConstraint(model_name="watchlist", constraint=models.UniqueConstraint(fields=("user","movie"), name="unique_watchlist_movie")),
    ]
