from flask_appbuilder import Model
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class Language(Model):
    id = Column(Integer, primary_key=True)
    wiki_id = Column(String(100), unique=True)
    label = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.label


class Genre(Model):
    id = Column(Integer, primary_key=True)
    wiki_id = Column(String(100), unique=True)
    label = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.label


class Country(Model):
    id = Column(Integer, primary_key=True)
    wiki_id = Column(String(100), unique=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Person(Model):
    id = Column(Integer, primary_key=True)
    wiki_id = Column(String(100), unique=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class ReviewScore(Model):
    __table_args__ = (UniqueConstraint("movie_id", "score", name="movie_score_uc"),)

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=False)
    movie = relationship("Movie", backref="reviews")
    score = Column(String(50), nullable=False)

    def __repr__(self):
        return self.score


movie_genre = Table(
    "movie_genre",
    Model.metadata,
    Column("movie_id", ForeignKey("movie.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)

movie_actor = Table(
    "movie_actor",
    Model.metadata,
    Column("movie_id", ForeignKey("movie.id"), primary_key=True),
    Column("actor_id", ForeignKey("person.id"), primary_key=True),
)


class Movie(Model):
    id = Column(Integer, primary_key=True)
    wiki_id = Column(String(100), unique=True)
    title = Column(String(100))
    description = Column(String(255))
    duration = Column(Integer)
    release_date = Column(DateTime)
    official_website = Column(String(100))
    imdb_id = Column(String(50))
    genres = relationship("Genre", secondary=movie_genre)
    actors = relationship("Person", secondary=movie_actor)

    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    country = relationship("Country")

    language_id = Column(Integer, ForeignKey("language.id"), nullable=False)
    language = relationship("Language")

    director_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    director = relationship("Person", foreign_keys=[director_id])

    producer_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    producer = relationship("Person", foreign_keys=[producer_id])
