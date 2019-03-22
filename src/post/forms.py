from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length
# from login.models import User

lengthErrorMessage = "Post should be between %(min)d and %(max)d characters!"

class PostForm(FlaskForm):
	postText = TextAreaField("Type Your Post", validators=[DataRequired(), Length(min=1, max=144, message=lengthErrorMessage)])
	submit = SubmitField("Submit Post")