from flask_wtf import FlaskForm
from wtforms import SubmitField

class LocationForm(FlaskForm):
	submit = SubmitField("See Others On Map")