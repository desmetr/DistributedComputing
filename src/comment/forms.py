from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length

lengthErrorMessage = "Comment should be between %(min)d and %(max)d characters!"

class CommentForm(FlaskForm):
	commentText = TextAreaField("Type Your Comment", validators=[Length(min=1, max=144, message=lengthErrorMessage)])
	submit = SubmitField("Submit Comment")