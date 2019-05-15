#To hold database model
from garden import db
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, Length

class Garden(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    vegetable = db.Column(db.String(20))
    fruits = db.Column(db.String(120))
    herbs = db.Column(db.String(120))
    User_id = db.Column(db.Integer)
    Img_id = db.Column(db.Integer)

    def __repr__(self):
        return f"garden('{self.vegetable}','{self.fruits}','{self.herbs}')"





