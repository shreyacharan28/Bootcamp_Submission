from django.db.models import Q

def global_search(query):
    from core.models import Movie, Actor, Director, Genre, Article
    q = query.strip()
    if not q:
        return {}
    return {
        "movies": Movie.objects.filter(Q(title__icontains=q) | Q(keywords__icontains=q))[:10],
        "actors": Actor.objects.filter(name__icontains=q)[:10],
        "directors": Director.objects.filter(name__icontains=q)[:10],
        "genres": Genre.objects.filter(name__icontains=q)[:10],
        "articles": Article.objects.filter(Q(title__icontains=q) | Q(tags__icontains=q))[:10],
    }
