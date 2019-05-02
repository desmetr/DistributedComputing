from flask import Flask
from newsfeed.config import Config

newsfeedApp = Flask(__name__, static_url_path=Config.STATIC_PATH_PHOTO)
newsfeedApp.config.from_object(Config)

from newsfeed import routes