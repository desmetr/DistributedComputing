from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField, SubmitField
from wtforms.validators import DataRequired, Length

class GroceryForm(FlaskForm):
    User_id = IntegerField('User_id', validators=[Length(min=3, max=20)])
    vegetable = StringField('vegetable',
                            validators=[DataRequired(), Length(min=3, max = 20)])
    fruits = StringField('fruits',
                            validators=[DataRequired(), Length(min=3, max=20)])
    herbs = StringField('herbs',
                            validators=[DataRequired(), Length(min=2, max=20)])
    #Img_id= IntegerField('Img_id',validators=[Length(min=2, max=20)])

    add = SubmitField("Add")