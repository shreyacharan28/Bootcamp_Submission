from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import date
from decimal import Decimal
from core.models import *

class Command(BaseCommand):
    help = "Seed Movie AI Hub with realistic demo data."

    def handle(self, *args, **options):
        genre_names = ["Action","Adventure","Animation","Comedy","Crime","Drama","Fantasy","Horror","Mystery","Romance","Science Fiction","Thriller"]
        genres = {n: Genre.objects.get_or_create(name=n, defaults={"description": f"{n} entertainment content."})[0] for n in genre_names}

        directors_data = [
            ("Christopher Nolan","British-American filmmaker known for ambitious, nonlinear storytelling.","United Kingdom"),
            ("Steven Spielberg","American filmmaker with a broad filmography across drama, adventure and science fiction.","United States"),
            ("Greta Gerwig","American filmmaker and actor known for character-driven stories.","United States"),
            ("Denis Villeneuve","Canadian filmmaker known for visually rich science fiction and drama.","Canada"),
        ]
        directors = {}
        for name, bio, nation in directors_data:
            directors[name] = Director.objects.get_or_create(name=name, defaults={"biography":bio,"nationality":nation})[0]

        actor_names = ["Tom Hanks","Leonardo DiCaprio","Matthew McConaughey","Anne Hathaway","Cillian Murphy","Emily Blunt","Margot Robbie","Robert Downey Jr.","Zendaya","Timothée Chalamet","Harrison Ford","Meryl Streep"]
        actors = {n: Actor.objects.get_or_create(name=n, defaults={"biography":f"Demo profile for {n}.","nationality":"United States"})[0] for n in actor_names}

        movies = [
            ("Interstellar","christopher-nolan",date(2014,11,7),169,8.7,1500,900000000,250000000,"A team travels beyond known space to search for a future for humanity.","Christopher Nolan",["Matthew McConaughey","Anne Hathaway"],["Science Fiction","Drama","Adventure"],"space time gravity future astronaut"),
            ("Inception","inception",date(2010,7,16),148,8.8,2100,839000000,160000000,"A skilled extractor enters dreams to plant an idea.","Christopher Nolan",["Leonardo DiCaprio","Tom Hanks"],["Science Fiction","Thriller","Action"],"dream mind heist reality"),
            ("The Dark Knight","the-dark-knight",date(2008,7,18),152,9.0,3200,1005000000,185000000,"Batman faces a criminal mastermind who pushes Gotham into chaos.","Christopher Nolan",["Cillian Murphy","Tom Hanks"],["Action","Crime","Drama"],"batman joker crime hero"),
            ("Jurassic Park","jurassic-park",date(1993,6,11),127,8.2,1800,1100000000,63000000,"Scientists create a theme park of cloned dinosaurs with dangerous consequences.","Steven Spielberg",["Harrison Ford"],["Adventure","Science Fiction"],"dinosaurs park science adventure"),
            ("E.T.","et",date(1982,6,11),115,7.9,1200,800000000,10500000,"A child befriends a stranded visitor from another world.","Steven Spielberg",["Harrison Ford"],["Science Fiction","Adventure","Family"],"alien child friendship space"),
            ("Dune: Part Two","dune-part-two",date(2024,3,1),166,8.6,1700,700000000,190000000,"Paul Atreides unites with Chani and the Fremen while seeking justice.","Denis Villeneuve",["Timothée Chalamet","Zendaya"],["Science Fiction","Adventure","Drama"],"desert prophecy empire sand"),
            ("Barbie","barbie",date(2023,7,21),114,7.0,1900,1446000000,145000000,"Barbie leaves her perfect world and discovers a more complicated reality.","Greta Gerwig",["Margot Robbie","Ryan Gosling"],["Comedy","Fantasy","Drama"],"barbie identity comedy pink"),
            ("Oppenheimer","oppenheimer",date(2023,7,21),180,8.9,2300,975000000,100000000,"A scientific and political portrait of the creation of the atomic bomb.","Christopher Nolan",["Cillian Murphy","Emily Blunt"],["Drama","History","Thriller"],"science history war atomic physics"),
            ("Catch Me If You Can","catch-me-if-you-can",date(2002,12,25),141,8.1,1100,352000000,52000000,"A young con artist stays ahead of an FBI agent while reinventing himself.","Steven Spielberg",["Tom Hanks","Leonardo DiCaprio"],["Crime","Drama","Comedy"],"con artist FBI identity chase"),
            ("The Prestige","the-prestige",date(2006,10,20),130,8.5,1300,109000000,40000000,"Two rival magicians become consumed by their competition.","Christopher Nolan",["Hugh Jackman","Christian Bale"],["Drama","Mystery","Thriller"],"magic rivalry mystery illusion"),
        ]
        for title, slug, rel, runtime, rating, votes, revenue, budget, synopsis, director, cast_names, genre_list, keywords in movies:
            m, _ = Movie.objects.get_or_create(slug=slug, defaults={
                "title":title,"release_date":rel,"runtime":runtime,"average_rating":rating,"vote_count":votes,
                "box_office_revenue":Decimal(revenue),"budget":Decimal(budget),"synopsis":synopsis,
                "director":directors[director],"keywords":keywords,"popularity":rating*10 + votes/100,
                "language":"English","country":"United States","status":"released","certification":"PG-13"
            })
            m.director = directors[director]
            m.cast.set([actors[n] for n in cast_names if n in actors])
            m.genres.set([genres[n] for n in genre_list if n in genres])
            m.save()
            BoxOffice.objects.get_or_create(movie=m, defaults={
                "opening_weekend":Decimal(revenue)*Decimal("0.12"),
                "domestic_revenue":Decimal(revenue)*Decimal("0.42"),
                "international_revenue":Decimal(revenue)*Decimal("0.58"),
                "worldwide_revenue":Decimal(revenue)
            })
            Review.objects.get_or_create(movie=m, title="Audience perspective", defaults={
                "reviewer_name":"Demo Reviewer","text":"Excellent movie with strong storytelling and memorable performances. Highly enjoyable.",
                "rating":min(10, round(rating)), "sentiment":"positive","sentiment_score":0.8
            })

        articles = [
            ("How Movie Ratings Shape Discovery","how-movie-ratings-shape-discovery","Movies use ratings, votes and popularity together to create a richer discovery experience.","analysis"),
            ("Understanding Box Office Performance","understanding-box-office-performance","A practical look at budget, opening weekend and worldwide revenue.","box_office"),
            ("How Recommendation Engines Find Similar Movies","how-recommendation-engines-find-similar-movies","Content similarity can combine genres, cast, directors, keywords and language.","ai"),
        ]
        for title, slug, summary, cat in articles:
            Article.objects.get_or_create(slug=slug, defaults={"title":title,"summary":summary,"content":summary+" This demo article explains the concept in a simple, structured way.","category":cat,"tags":"movies,analytics,AI"})

        self.stdout.write(self.style.SUCCESS("Movie AI Hub demo data seeded successfully."))
