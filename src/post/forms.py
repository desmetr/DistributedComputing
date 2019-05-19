from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError, Length, Optional

lengthErrorMessage = "Post should be between %(min)d and %(max)d characters!"

class PostForm(FlaskForm):
	postText = TextAreaField("Type Your Post", validators=[DataRequired(), Length(min=1, max=144, message=lengthErrorMessage)])
	image = FileField(u'Image File',[Optional()])
	submit = SubmitField("Submit Post")
	comment = SubmitField("Add Comment")
	

class PostFormAfterCheck(FlaskForm):
	submitAfterCheck = SubmitField("Submit Post Anyway")
	discardAfterCheck = SubmitField("Discard Post")
