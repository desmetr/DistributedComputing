#initialize application

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SECRET_KEY']='\xc8/3\xad\xf5\xe5\xf5,\xb1\x9ck\xab\xbc\xa5\x9a\xad9\xbf\x1dCm\xc2\xe2\xb4'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

from garden import routes
