# Movie AI Hub

A production-style Django movie analytics and AI discovery platform.

## Features
- Movie, actor, director and genre modules
- Ratings, reviews and local sentiment analysis
- Box-office analytics
- Trending and popularity ranking
- Content-based movie recommendations
- Global search
- Local AI movie assistant with intent detection
- AI personas and explanation levels
- REST APIs with Django REST Framework
- Django Admin
- Responsive cinematic UI
- SQLite
- Pytest / pytest-django
- Demo data seeding

## Install — Windows PowerShell, without venv

```powershell
cd movie_ai_hub
py --version
py -m pip install -r requirements.txt
copy .env.example .env
py manage.py check
py manage.py makemigrations
py manage.py migrate
py manage.py seed_data
py -m pytest
py manage.py createsuperuser
py manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## AI
POST `/api/ai/ask/`

Example:
```json
{
  "question": "Recommend movies similar to Interstellar.",
  "persona": "Casual Movie Fan",
  "level": "Beginner"
}
```

The initial AI implementation is local and requires no API key. It detects intents and queries the Django database. The recommendation service uses movie metadata including genres, cast, director, language and keywords.

## APIs
- `/api/movies/`
- `/api/actors/`
- `/api/directors/`
- `/api/genres/`
- `/api/ratings/`
- `/api/reviews/`
- `/api/box-office/`
- `/api/articles/`
- `/api/ai/ask/`
- `/api/statistics/`
- `/api/trending/`
- `/api/movies/<id>/recommendations/`

## Troubleshooting

### Python not recognized
Use:
`py --version`

### pip problem
Use:
`py -m pip install -r requirements.txt`

### Migration problem
Use:
`py manage.py makemigrations`
`py manage.py migrate`

### Port already in use
Use:
`py manage.py runserver 8001`

### Test problem
Use:
`py -m pytest`

### AI API key
No external key is required for the local AI implementation.

## Project structure

The project separates models, views, APIs, templates, static assets and domain services for AI, recommendations, sentiment, statistics and search.
