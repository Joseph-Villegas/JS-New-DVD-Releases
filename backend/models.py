from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autoflush": False})

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column('id', db.Integer, autoincrement=True, primary_key=True)
    imdb_id = Column('imdb_id', db.String(255), nullable=False, unique=True)
    tmdb_id = Column('tmdb_id', db.Integer, nullable=False, unique=True)
    title = Column('title', db.String(255), nullable=False)
    poster = Column('poster', db.String(255), nullable=False)
    overview = Column('overview', db.Text, nullable=False)
    rating = Column('rating', db.Float, nullable=False)
    release_week = Column('release_week', db.String(255), nullable=False)

    def __init__(self, imdb_id, tmdb_id, title, poster, overview, rating, release_week):
        self.imdb_id = imdb_id
        self.tmdb_id = tmdb_id
        self.title = title
        self.poster = f'https://image.tmdb.org/t/p/w342{poster}'
        self.overview = overview
        self.rating = rating
        self.release_week = release_week
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.imdb_id}', {self.tmdb_id}, '{self.title}', '{self.poster}', '{self.overview}', {self.rating}, '{self.release_week}')"    
    
    def __str__(self):
        return f'{{ "id": "{self.id}", "imdb_id": "{self.imdb_id}", "tmdb_id": "{self.tmdb_id}", "title": "{self.title}", "poster": "{self.poster}", "overview": "{self.overview}", "rating": "{self.rating}", "release_week": "{self.release_week}"}}'
   
    def __itr__(self):
        for column in self.__table__.columns:
            yield column.name, getattr(self, column.name)