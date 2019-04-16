from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from post.config import Config

postApp = Flask(__name__)
postApp.config.from_object(Config)

postDB = SQLAlchemy(postApp)
migrate = Migrate(postApp, postDB)

# post = LoginManager(postApp)
# login.login_view = "login"

from post import routes