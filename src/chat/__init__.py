#initialize application

from flask import Flask

chatApp=Flask(__name__)

from chat import routes
