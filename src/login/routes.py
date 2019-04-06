from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
# from __init__ import loginApp, loginDB
from login import loginApp, loginDB
# from forms import LoginForm, RegistrationForm
from login.forms import LoginForm, RegistrationForm
# from models import User
from login.models import User
from werkzeug.urls import url_parse

@loginApp.route("/")
@loginApp.route("/index")
@login_required
def index():
	posts = [
		{
			"author": {"username": "John"},
			"body": "Beautiful day in Portland!"
		},
		{
			"author": {"username": "Susan"},
			"body": "The Avengers movie was so cool!"
		}
	]
	return render_template("index.html", title="Home", posts=posts)

@loginApp.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password")
			return redirect(url_for("login"))

		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get("next")
		if not next_page or url_parse(next_page).netloc != "":
			next_page = url_for("index")
		
		return redirect(next_page)

	return render_template("login.html", title="Sign In", form=form)

@loginApp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))

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
		return redirect(url_for("login"))

	return render_template("register.html", title="Register", form=form)

@loginApp.route("/users", methods=["GET"])
def getUsers():
	users = User.query.all()
	return jsonify([User.serialize(user) for user in users])

@loginApp.route("/users/<user_id>", methods=["GET"])
def getSingleUser(user_id):
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


if __name__ == "__main__":
	loginApp.run(debug=True)