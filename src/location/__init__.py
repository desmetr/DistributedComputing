from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from location.config import Config

locationApp = Flask(__name__)
locationApp.config.from_object(Config)

from location import routes