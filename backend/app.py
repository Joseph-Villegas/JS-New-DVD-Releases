import os
import atexit
import asyncio
import aiohttp
import requests
from scraper import scrape
from models import db, Movie
from flask import Flask, jsonify, request, abort
from apscheduler.schedulers.background import BackgroundScheduler

# app = Flask(__name__)
# app = Flask(__name__, static_folder='./build', static_url_path='/')
app = Flask(__name__, static_folder='./frontend/public', static_url_path='/')


# SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/all-releases', methods=['GET'])
def all_releases():
    if request.method != "GET":
        abort(404)

    try:
        movies = [dict(movie) for movie in db.session.query(Movie).all()]
        return jsonify({'success': True, 'message': 'Query processed', 'query_results': movies}), 200
    except Exception as e:
        print(f"Error: {e}", flush=True)
        return jsonify({'success': False, 'message': 'Error processing query'}), 400
    finally:
        db.session.close()

@app.route('/api/this-weeks-releases', methods=['GET'])
def this_week():
    if request.method != "GET":
        abort(404)
    
    return jsonify({ 'success': True, 'message': 'Query processed', 'query_results': get_by_week('this week') }), 200

@app.route('/api/last-weeks-releases', methods=['GET'])
def last_week():
    if request.method != "GET":
        abort(404)
    
    return jsonify({ 'success': True, 'message': 'Query processed', 'query_results': get_by_week('last week') }), 200

@app.route('/api/next-weeks-releases', methods=['GET'])
def next_week():
    if request.method != "GET":
        abort(404)
    
    return jsonify({ 'success': True, 'message': 'Query processed', 'query_results': get_by_week('next week') }), 200

"""
    Get all movies in the database whose release week matches the given query.
"""
def get_by_week(week):
    with app.app_context():
        try:
            movies = Movie.query.filter(Movie.release_week.like(f"%{week}%")).all()
            return [dict(movie) for movie in movies]
        except Exception as e:
            print(f"Error: {e}", flush=True)
            return []
        finally:
            db.session.close()

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

# Create schedule for mailing status report
scheduler = BackgroundScheduler()
scheduler.start()

scheduler.add_job(func=scrape_n_save, id='cron_scrape_n_save', name='Update DB with new releases every hour', trigger='cron', hour='*') 

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))