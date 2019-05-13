from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
# from __init__ import loginApp, loginDB
from login import loginApp, loginDB
# from forms import LoginForm, RegistrationForm
from login.forms import LoginForm, RegistrationForm
# from models import User
from login.models import User, Friendship
from werkzeug.urls import url_parse
import urlsConfig

@loginApp.route("/login", methods=["GET", "POST"])
def login():
	# if current_user.is_authenticated:
	# 	return redirect(response)

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password")
			return redirect(url_for("login"))

		login_user(user, remember=form.remember_me.data)
		
		response = redirect(urlsConfig.URLS['newsfeed_url'])
		response.set_cookie("currentSessionCookie", str(user.id))
		return response	

	return render_template("login.html", title="Sign In", form=form)

@loginApp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("login"))

@loginApp.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, location=form.location.data)
		user.set_password(form.password.data)
		user.calculateLatLng()

		loginDB.session.add(user)
		loginDB.session.commit()

		flash("Congratulations, you are a new registered user!")
		response = redirect(urlsConfig.URLS['newsfeed_url'])
		response.set_cookie("currentSessionCookie", str(user.id))
		return response	

	return render_template("register.html", title="Register", form=form)

@loginApp.route("/users", methods=["GET"])
def getUsers():
	users = User.query.all()
	return jsonify([User.serialize(user) for user in users])

@loginApp.route("/user", methods=["GET"])
def getSingleUser():
	user_id = request.args.get('user_id')
	response_object = {
		'status': 'fail',
		'message': 'User does not exist'
	}

	try:
		user = User.query.filter_by(id=int(user_id)).first()
		if not user:
			return jsonify(response_object), 404
		else:
			response_object = {
				'status': 'success',
				'data': {
					'id': user.id,
					'username': user.username,
					'email': user.email,
					'location': user.location,
				}
			}
			return jsonify(response_object), 200
	except ValueError:
		return jsonify(response_object), 404

@loginApp.route("/friendship", methods=["GET"])
def friendship():
	other_user_id = int(request.args.get('other_user'))
	response_object = {
		'status': 'fail',
		'message': 'User does not exist'
	}

	# if current_user.is_authenticated:
	if current_user.id != other_user:
		friendship = Friendship(user1=current_user.id, user2=other_user_id)

		loginDB.session.add(friendship)
		loginDB.session.commit()

	response = redirect(urlsConfig.URLS['location_url'])
	response.set_cookie("currentSessionCookie", str(user.id))
	return response	

@loginApp.route("/unfriend", methods=["GET"])
def unfriend():
	other_user_id = int(request.args.get('other_user'))

	if current_user.id != other_user:
		friendship = Friendship.query.filter_by(user1=user).filter_by(user2=user2).first()

		loginDB.session.delete(friendship)
		loginDB.session.commit()

	response = redirect(urlsConfig.URLS['location_url'])
	response.set_cookie("currentSessionCookie", str(user.id))
	return response	

@loginApp.route("/getFriendship", methods=["GET"])
def getFriendship():
	user1 = request.args.get('user1')
	user2 = request.args.get('user2')

	if user1 != user2:
		friendship = Friendship.query.filter_by(user1=user).filter_by(user2=user2).first()
		if friendship:
			print("Friendship exists already")
			return True
	else:
		return False

if __name__ == "__main__":
	loginApp.run(debug=True)