# install Flask SQLAlchemy and Flask Migrate!
# from __init__ import loginDB, login
from login import loginDB, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from login.key import key
import requests

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

class User(UserMixin, loginDB.Model):
	id = loginDB.Column(loginDB.Integer, primary_key=True)
	username = loginDB.Column(loginDB.String(64), index=True, unique=True)
	email = loginDB.Column(loginDB.String(120), index=True, unique=True)
	password_hash = loginDB.Column(loginDB.String(128))
	location = loginDB.Column(loginDB.String(128))
	lat = loginDB.Column(loginDB.Float)
	lng = loginDB.Column(loginDB.Float)
	admin = loginDB.Column(loginDB.Boolean, default=False)

	def __repr__(self):
		return "<User {}, id = {} , {}, admin = {}>".format(self.username, self.id, self.location, self.admin)

	def calculateLatLng(self):
		search_payload = {"key" : key, "query" : self.location}
		search_request = requests.get(search_url, params=search_payload)
		search_json = search_request.json()

		location = search_json["results"][0]["geometry"]["location"]
		self.lat = location["lat"]
		print(self.lat)
		self.lng = location["lng"]
		print(self.lng)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def serialize(self):
		return {
			"id": self.id,
			"username": self.username,
			"email": self.email,
			"location": self.location,
			"lat": self.lat,
			"lng": self.lng,
			"admin": self.admin
		}

class Friendship(UserMixin, loginDB.Model):
	id = loginDB.Column(loginDB.Integer, primary_key=True)
	user1 = loginDB.Column(loginDB.Integer, loginDB.ForeignKey('user.id'))
	user2 = loginDB.Column(loginDB.Integer, loginDB.ForeignKey('user.id'))

	def __repr__(self):
		return "<Friendship {}, {}>".format(self.user1, self.user2)

	def serialize(self):
		return {
			"id": self.id,
			"user1": self.user1,
			"user2": self.user2
		}

@login.user_loader
def load_user(id):
	return User.query.get(int(id))