import os

from flask_appbuilder.security.manager import AUTH_DB

basedir = os.path.abspath(os.path.dirname(__file__))

# Your App secret key
SECRET_KEY = "\x05\xa7\xaf>m\xd2:SL\xc3C?\xfbm\xa3\x95\xe6|\x19\xca\xbc\xb1\x823ecd2720a21821e380171e2181e9b0d8336d8"

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "sqlite:////home/app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-WTF flag for CSRF
CSRF_ENABLED = True

# ------------------------------
# GLOBALS FOR APP Builder
# ------------------------------
# Uncomment to setup Your App name
APP_NAME = "Movies Data"

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
AUTH_TYPE = AUTH_DB
