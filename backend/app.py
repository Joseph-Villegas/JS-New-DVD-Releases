from flask import Flask, jsonify
from scraper import scrape, search_by_week
from models import db, Movie
import os
import json

# https://api.themoviedb.org/3/find/tt0076759?api_key=927dd7ea98fd5ba426ffb8fb1f2c88d0&language=en-US&external_source=imdb_id
# import requests

# x = requests.get('https://w3schools.com')
# print(x.status_code)

# >>> payload = {'key1': 'value1', 'key2': 'value2'}
# >>> r = requests.get('https://httpbin.org/get', params=payload)

# print(r.url)
# r.text
# r.encoding
# r.json()

app = Flask(__name__)

# SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=['GET'])
def home():
    return "<h1>DVD Release Dates API</h1> \
        <p>This API retrieves retail release schedules for DVDs by performing a web scrape</p> \
        <p>Source: https://www.dvdsreleasedates.com</p> \
        <p>(Upcoming) Try these endpoints: /this-week, /last-week, /next-week, /in-two-weeks, /all-weeks</p>"

if __name__ == "__main__":
    app.run()

# Example request response from quering the TMDb API for a movie given its IMDb ID
# {
#   "movie_results": [
#     {
#       "vote_average": 8.2,
#       "overview": "Princess Leia is captured and held hostage by the evil Imperial forces in their effort to take over the galactic Empire. Venturesome Luke Skywalker and dashing captain Han Solo team together with the loveable robot duo R2-D2 and C-3PO to rescue the beautiful princess and restore peace and justice in the Empire.",
#       "release_date": "1977-05-25",
#       "adult": false,
#       "backdrop_path": "/4qCqAdHcNKeAHcK8tJ8wNJZa9cx.jpg",
#       "vote_count": 15455,
#       "genre_ids": [
#         12,
#         28,
#         878
#       ],
#       "id": 11,
#       "original_language": "en",
#       "original_title": "Star Wars",
#       "poster_path": "/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg",
#       "title": "Star Wars",
#       "video": false,
#       "popularity": 59.544
#     }
#   ],
#   "person_results": [],
#   "tv_results": [],
#   "tv_episode_results": [],
#   "tv_season_results": []
# }

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
