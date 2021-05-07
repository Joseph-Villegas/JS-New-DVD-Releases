import os
import asyncio
import aiohttp
import requests
from scraper import scrape
from models import db, Movie
from flask import Flask, jsonify

app = Flask(__name__)

# SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')

@app.route('/', methods=['GET'])
def home():
    return "<h1>DVD Release Dates API</h1> \
        <p>This API retrieves retail release schedules for DVDs by performing a web scrape</p> \
        <p>Source: https://www.dvdsreleasedates.com</p> \
        <p>(Upcoming) Try these endpoints: /this-week, /last-week, /next-week, /in-two-weeks, /all-weeks</p>"

"""
    An application factory for tethering a database to SQLAlchemy models.
    For use in initialization or updates.
    In practice:
        Load in environment variables
        Navigate to the backend directory
        Import this function and run through a Python interactive session
        1. >>> from app import create_app
        2. >>> from models import db      
        3. >>> db.create_all(app=create_app())
"""
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', '')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app

"""
    Perform a fetch request to the TMDb API, gathering information for a film by its IMDb ID.
    Then place this film, along with its release week and IMDb ID, in the database.
"""
async def fetch(session, release_week, imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&language=en-US&external_source=imdb_id"
    async with session.get(url) as response:
        data = await response.json()

        movie_results = data['movie_results']
        tv_results = data['tv_results']

        if len(movie_results) != 0:
            movie = movie_results[0]
            with app.app_context():
                try:
                    db.session.add(Movie(imdb_id, 
                                        movie['id'], 
                                        movie['title'], 
                                        movie['poster_path'], 
                                        movie['overview'], 
                                        movie['vote_average'], 
                                        release_week))
                    db.session.commit()
                except Exception as e:
                    print(f"Error: {e}", flush=True)
                finally:
                    db.session.close()
        elif len(tv_results) !=0:
            show = tv_results[0]
            with app.app_context():
                try:
                    db.session.add(Movie(imdb_id, 
                                        show['id'], 
                                        show['name'], 
                                        show['poster_path'], 
                                        show['overview'], 
                                        show['vote_average'], 
                                        release_week))
                    db.session.commit()
                except Exception as e:
                    print(f"Error: {e}", flush=True)
                finally:
                    db.session.close()
        else:
            pass

"""
    Gather all fetch requests to the TMDb API as tasks to be performed at once.
    Then perform tasks.
"""
async def get_tmdb_data(movies):
    async with aiohttp.ClientSession() as session:
        with app.app_context():
            Movie.query.delete()
        tasks = [fetch(session, release_week, imdb_id) for release_week, imdb_id in movies]
        await asyncio.gather(*tasks)

"""
    Perform a webscrape and organize data into a list of tuples containing the release week and IMDb ID for each movie.
    Then for each tuple, using asyncio, retrieve all film's TMDb information at once. 
"""
def scrape_n_save():
    movies = [(week['release_week'], movie['imdb_id']) for week in scrape() for movie in week['movies']]
    asyncio.get_event_loop().run_until_complete(get_tmdb_data(movies))

if __name__ == "__main__":
    app.run()