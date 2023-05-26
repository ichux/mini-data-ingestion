from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import Country, Genre, Language, Movie, Person, ReviewScore


class GenreModelView(ModelView):
    datamodel = SQLAInterface(Genre)
    list_columns = ["wiki_id", "label"]


class ReviewScoreModelView(ModelView):
    datamodel = SQLAInterface(ReviewScore)
    list_columns = ["score"]


class MovieModelView(ModelView):
    datamodel = SQLAInterface(Movie)
    list_columns = [
        "wiki_id",
        "title",
        "description",
        "duration",
        "release_date",
        "official_website",
        "imdb_id",
    ]

    related_views = [ReviewScoreModelView]


class CountryModelView(ModelView):
    datamodel = SQLAInterface(Country)
    list_columns = ["wiki_id", "name"]

    related_views = [MovieModelView]


class LanguageModelView(ModelView):
    datamodel = SQLAInterface(Language)
    list_columns = ["wiki_id", "label"]

    related_views = [MovieModelView]


class PersonModelView(ModelView):
    datamodel = SQLAInterface(Person)
    list_columns = ["wiki_id", "name"]

    related_views = [MovieModelView]


db.create_all()

appbuilder.add_view(GenreModelView, "Genres", icon="fa-folder-open-o", category="Data")
appbuilder.add_view(
    ReviewScoreModelView, "Review Scores", icon="fa-folder-open-o", category="Data"
)
appbuilder.add_view(MovieModelView, "Movies", icon="fa-folder-open-o", category="Data")
appbuilder.add_view(
    CountryModelView, "Countries", icon="fa-folder-open-o", category="Data"
)
appbuilder.add_view(
    LanguageModelView, "Languages", icon="fa-folder-open-o", category="Data"
)
appbuilder.add_view(PersonModelView, "People", icon="fa-folder-open-o", category="Data")
