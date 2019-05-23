from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from login import loginApp, loginDB
from login.forms import LoginForm, RegistrationForm
from login.models import User, Friendship
from werkzeug.urls import url_parse
from login import urlsConfig

@loginApp.route("/login", methods=["GET", "POST"])
def login():
	loginForm = LoginForm()
	if loginForm.validate_on_submit():
		user = User.query.filter_by(username=loginForm.username.data).first()

		if user is None or not user.check_password(loginForm.password.data):
			flash("Invalid username or password")
			return redirect(url_for("login"))

		login_user(user, remember=loginForm.remember_me.data)

		response = redirect(urlsConfig.URLS['newsfeed_url'])
		response.set_cookie("currentSessionCookie", str(user.id))
		return response	

	return render_template("login.html", title="Sign In", loginForm=loginForm)

@loginApp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("login"))

@loginApp.route("/register", methods=["GET", "POST"])
def register():	
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, location=form.location.data, admin=form.admin.data)
		user.set_password(form.password.data)
		user.calculateLatLng()

		loginDB.session.add(user)
		loginDB.session.commit()

		flash("Congratulations, you are a new registered user!")
		response = redirect(urlsConfig.URLS['newsfeed_url'])
		response.set_cookie("currentSessionCookie", str(user.id))
		return response	

	return render_template("register.html", title="Register", registerForm=form)

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
					'admin': user.admin,
				}
			}
			return jsonify(response_object), 200
	except ValueError:
		return jsonify(response_object), 404

@loginApp.route("/deleteUser", methods=['GET', 'POST', 'DELETE'])
def deleteUser():
    user_id = int(request.args.get('user_id'))
    user = User.query.filter_by(id=user_id).delete()
    loginDB.session.commit()
    return "OK"

@loginApp.route("/getAdmins", methods=["GET"])
def getAdmins():
	admins = User.query.filter_by(admin=True)
	return jsonify([User.serialize(admin) for admin in admins])

@loginApp.route("/friendship", methods=["GET"])
def friendship():
	other_user_id = int(request.args.get('other_user'))
	response_object = {
		'status': 'fail',
		'message': 'User does not exist'
	}

	if current_user.id != other_user_id:
		friendship = Friendship(user1=current_user.id, user2=other_user_id)

		loginDB.session.add(friendship)
		loginDB.session.commit()

	response = redirect(urlsConfig.URLS['location_url'])
	response.set_cookie("currentSessionCookie", str(current_user.id))
	return response	

@loginApp.route("/unfriend", methods=["GET"])
def unfriend():
	other_user_id = int(request.args.get('other_user'))

	if current_user.id != other_user_id:
		friendship = Friendship.query.filter_by(user1=current_user.id).filter_by(user2=other_user_id).first()

		loginDB.session.delete(friendship)
		loginDB.session.commit()

	response = redirect(urlsConfig.URLS['location_url'])
	response.set_cookie("currentSessionCookie", str(current_user.id))
	return response	

@loginApp.route("/getFriendship", methods=["GET"])
def getFriendship():
	user_id_1 = request.args.get('user1')
	user_id_2 = request.args.get('user2')

	if user_id_1 != user_id_2:
		friendship = Friendship.query.filter_by(user1=user_id_1).filter_by(user2=user_id_2).first()
		if friendship:
			print("Friendship exists already")
			return "OK"
	return "NOK"

@loginApp.route("/getAllFriends", methods=["GET"])
def getAllFriends():
	foundUser = User.query.filter(User.username=="b").first()
	print("foundUser:")
	print(foundUser)
	foundFriends = Friendship.query.filter((Friendship.user1 == foundUser.id) | (Friendship.user2 == foundUser.id)).all()
	print("friends:")
	friends=[]
	for friend in foundFriends:
		print(foundUser.id)
		print(friend.user1)
		print(friend.user2)
		
		if(foundUser.id == friend.user1):
			friends.append(friend.user2)
		else:
			friends.append(friend.user1)
	print(jsonify(friends))
	return jsonify(friends)

@loginApp.errorhandler(Exception)
def exceptionHandler(error):
	print(error)
	errorString = "Something went wrong! It seems there was a " + error.__class__.__name__ + " while making a request"
	if "post" in repr(error).lower():
		errorString += " to the Post service."
	elif "comment" in repr(error).lower():
		errorString += " to the Comment service."
	elif "photo" in repr(error).lower():
		errorString += " to the Photo service."
	elif "advertisements" in repr(error).lower():
		errorString += " to the Advertisement service."
	elif "user" in repr(error).lower():
		errorString += " to the Login service."
	else:
		errorString += "."
	return errorString


if __name__ == "__main__":
	loginApp.run(debug=True)