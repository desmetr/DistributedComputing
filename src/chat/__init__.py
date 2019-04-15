#initialize application

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__))


chatApp=Flask(__name__)
chatApp.config['SECRET_KEY']='\xc8/3\xad\xf5\xe5\xf5,\xb1\x9ck\xab\xbc\xa5\x9a\xad9\xbf\x1dCm\xc2\xe2\xb4'
chatApp.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'chatApp.db')
chatApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
chatDB=SQLAlchemy(chatApp)
migrate = Migrate(chatApp, chatDB)

from chat import routes