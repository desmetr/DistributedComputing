#initialize application

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

advApp=Flask(__name__)
advApp.config['SECRET_KEY']='\xc8/3\xad\xf5\xe5\xf5,\xb1\x9ck\xab\xbc\xa5\x9a\xad9\xbf\x1dCm\xc2\xe2\xb4'
advApp.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
advDB=SQLAlchemy(advApp)
migrate = Migrate(advApp, advDB)

from advertising import routes
