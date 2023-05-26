import logging

from flask import Flask
from flask_appbuilder import SQLA, AppBuilder

from ..wikidata import load_wikidata

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_object("mdi.config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


from . import views


@app.cli.command("data")
def load_wikidata_command():
    load_wikidata(db)
