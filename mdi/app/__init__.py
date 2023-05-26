import logging

from flask import Flask
from flask_appbuilder import SQLA, AppBuilder



"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("mdi.config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


from . import views
from ..wikidata import load_wikidata

@app.cli.command("data")
def load_wikidata_command():
    load_wikidata(db)
