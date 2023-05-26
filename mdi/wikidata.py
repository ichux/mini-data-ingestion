from datetime import datetime

import requests
from flask_appbuilder import SQLA

INSERT_LABELED_QUERY = """
INSERT INTO {table}(wiki_id, label)
VALUES
  (:wiki_id, :label) ON CONFLICT DO
UPDATE
SET
  label = EXCLUDED.label RETURNING id
"""

INSERT_NAMED_QUERY = """
INSERT INTO {table}(wiki_id, name)
VALUES
  (:wiki_id, :name) ON CONFLICT DO
UPDATE
SET
  name = EXCLUDED.name RETURNING id
"""

INSERT_GENRE_QUERY = """
INSERT INTO movie_genre(movie_id, genre_id)
VALUES
  (:movie_id, :genre_id) ON CONFLICT DO NOTHING
"""

INSERT_ACTOR_QUERY = """
INSERT INTO movie_actor(movie_id, actor_id)
VALUES
  (:movie_id, :actor_id) ON CONFLICT DO NOTHING
"""

INSERT_REVIEW_SCORE_QUERY = """
INSERT INTO review_score(movie_id, score)
VALUES
  (:movie_id, :score) ON CONFLICT DO NOTHING
"""

INSERT_MOVIE_QUERY = """
INSERT INTO movie(
  wiki_id, title, description, duration,
  release_date, imdb_id, official_website,
  language_id, country_id, producer_id,
  director_id
)
VALUES
  (
    :wiki_id, :title, :description, :duration,
    :release_date, :imdb_id, :official_website,
    :language_id, :country_id, :producer_id,
    :director_id
  ) ON CONFLICT DO
UPDATE
SET
  title = EXCLUDED.title,
  description = EXCLUDED.description,
  duration = EXCLUDED.duration,
  release_date = EXCLUDED.release_date,
  imdb_id = EXCLUDED.imdb_id,
  official_website = EXCLUDED.official_website,
  language_id = EXCLUDED.language_id,
  country_id = EXCLUDED.country_id,
  producer_id = EXCLUDED.producer_id,
  director_id = EXCLUDED.director_id RETURNING id
"""


def load_wikidata(db: SQLA):
    with open("query.sparql", "r") as query_file:
        query = query_file.read()

    response = requests.get(
        "https://query.wikidata.org/sparql",
        params={"query": query, "format": "json"},
    )

    response.raise_for_status()
    data = response.json()

    for item in data["results"]["bindings"]:
        cast_member = item["castMember"]["value"].split("/")[-1]
        cast_member_label = item["castMemberLabel"]["value"]
        country_of_origin = item["countryOfOrigin"]["value"].split("/")[-1]
        country_of_origin_label = item["countryOfOriginLabel"]["value"]
        director = item["director"]["value"].split("/")[-1]
        director_label = item["directorLabel"]["value"]
        duration = int(item["duration"]["value"])
        genre = item["genre"]["value"].split("/")[-1]
        genre_label = item["genreLabel"]["value"]
        imdb_id = item["imdbID"]["value"]
        movie = item["movie"]["value"].split("/")[-1]
        movie_description = item["movieDescription"]["value"]
        movie_title = item["movieTitle"]["value"]
        official_website = item["officialWebsite"]["value"]
        original_language = item["originalLanguage"]["value"].split("/")[-1]
        original_language_label = item["originalLanguageLabel"]["value"]
        producer = item["producer"]["value"].split("/")[-1]
        producer_label = item["producerLabel"]["value"]
        publication_date = datetime.strptime(
            item["publicationDate"]["value"], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%Y-%m-%d %H:%M:%S")
        review = item["review"]["value"].strip()

        language_id = db.session.execute(
            INSERT_LABELED_QUERY.format(table="language"),
            {"label": original_language_label, "wiki_id": original_language},
        ).scalar()

        genre_id = db.session.execute(
            INSERT_LABELED_QUERY.format(table="genre"),
            {"label": genre_label, "wiki_id": genre},
        ).scalar()

        country_id = db.session.execute(
            INSERT_NAMED_QUERY.format(table="country"),
            {"name": country_of_origin_label, "wiki_id": country_of_origin},
        ).scalar()

        producer_id = db.session.execute(
            INSERT_NAMED_QUERY.format(table="person"),
            {"name": producer_label, "wiki_id": producer},
        ).scalar()

        director_id = db.session.execute(
            INSERT_NAMED_QUERY.format(table="person"),
            {"name": director_label, "wiki_id": director},
        ).scalar()

        actor_id = db.session.execute(
            INSERT_NAMED_QUERY.format(table="person"),
            {"name": cast_member_label, "wiki_id": cast_member},
        ).scalar()

        movie_id = db.session.execute(
            INSERT_MOVIE_QUERY,
            {
                "wiki_id": movie,
                "title": movie_title,
                "description": movie_description,
                "duration": duration,
                "release_date": publication_date,
                "imdb_id": imdb_id,
                "official_website": official_website,
                "language_id": language_id,
                "country_id": country_id,
                "producer_id": producer_id,
                "director_id": director_id,
            },
        ).scalar()

        db.session.execute(
            INSERT_GENRE_QUERY,
            {"movie_id": movie_id, "genre_id": genre_id},
        )

        db.session.execute(
            INSERT_ACTOR_QUERY,
            {"movie_id": movie_id, "actor_id": actor_id},
        )

        db.session.execute(
            INSERT_REVIEW_SCORE_QUERY,
            {"movie_id": movie_id, "score": review},
        )

        db.session.commit()
