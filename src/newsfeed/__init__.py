from flask import Flask
from newsfeed.config import Config

newsfeedApp = Flask(__name__)
newsfeedApp.config.from_object(Config)

from newsfeed import routes