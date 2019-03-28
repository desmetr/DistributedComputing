from photo import photoDB
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin

class Photo(photoDB.Model):
	id = photoDB.Column(photoDB.Integer, primary_key=True)
	url = photoDB.Column(photoDB.String(144), index=True)
	filename = photoDB.Column(photoDB.String(144), index=True)
	user = photoDB.Column(photoDB.String(64), index=True)

	def __repr__(self):
		return "<Photo {}, filename={}>".format(self.id, self.filename)

	def serialize(self):
		return {
			"id": self.id,
			"url": self.url,
			"filename": self.filename,
			"user": self.user,
		}		