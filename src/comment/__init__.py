from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from comment.config import Config

commentApp = Flask(__name__)
commentApp.config.from_object(Config)

commentDB = SQLAlchemy(commentApp)
migrate = Migrate(commentApp, commentDB)

from comment import routes