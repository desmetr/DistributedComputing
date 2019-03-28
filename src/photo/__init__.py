from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

photoApp = Flask(__name__)
photoApp.config.from_object(Config)

photoDB = SQLAlchemy(photoApp)
migrate = Migrate(photoApp, photoDB)

# photo = LoginManager(photoApp)
# login.login_view = "login"

from photo import routes