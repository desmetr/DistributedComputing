from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from wtforms.validators import DataRequired, ValidationError
# from login.models import User

class PhotoForm(FlaskForm):
	file = FileField(validators=[FileRequired()])
	submit = SubmitField("Submit Photo")