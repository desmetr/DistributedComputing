from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField,FileField
from wtforms.validators import InputRequired,Optional, ValidationError, Length

lengthErrorMessage = "Post should be between %(min)d and %(max)d characters!"

class AdvertisementForm(FlaskForm):
	tag=StringField("Type your tag here",[InputRequired()])
	advertisementText = TextAreaField("Type the advertisement text here",[Optional()])
	image = FileField(u'Image File',[Optional()])
	source = StringField("Type the source url here", [InputRequired()])
	submit = SubmitField("Submit advertisement")
