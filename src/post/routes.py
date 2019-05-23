from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from post import postApp, postDB
from post.forms import PostForm, PostFormAfterCheck
from post.models import Post
from werkzeug.urls import url_parse
from sqlalchemy import desc
from datetime import datetime
import requests
import itertools
from post import urlsConfig
import json
import urllib.request
import base64
postText = ""

current_user_id=""

@postApp.route("/getAllPosts", methods=["GET"])
def getAllPosts():
	posts = Post.query.order_by(desc(Post.timestamp)).all()
	return jsonify([Post.serialize(post) for post in posts])

@postApp.route("/post", methods=["GET", "POST"])
def makePost():
	global current_user_id, postText
	current_user_id = request.cookies.get("currentSessionCookie")
	if current_user_id:
		# Get current user information
		current_user_response = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id))

		if current_user_response.status_code == 200:

			postForm = PostForm()
			postFormAfterCheck = PostFormAfterCheck()

			if postForm.validate_on_submit():
				postText = postForm.postText.data
				image = ""
				if postForm.image.data:
					image = base64.b64encode(postForm.image.data.read()).decode('utf-8')

				response = requests.post(urlsConfig.URLS['profanity_url'], params={'text': postText})

				# Only show div is post contained a bad word
				if response.text == "BAD":
					return render_template("post.html", title="Post", postForm=postForm, postFormAfterCheck=postFormAfterCheck, display='', submitted="false")
				elif response.text == "GOOD":
					print("postReading")
					post = Post(postText=postText, user="2", timestamp=datetime.now(),image=image)
					postDB.session.add(post)
					postDB.session.commit()
					flash("Successfully created a new post!")
					#return redirect(urlsConfig.URLS['newsfeed_url'])
					users = json.loads(urllib.request.urlopen(urlsConfig.URLS['allFriends_url']).read())
					print(users)
					postJson = json.dumps({"postText":post.postText,"user":post.user, "friends":users})
					print(postJson)
					return render_template("post.html", title="Post", postForm=postForm, postFormAfterCheck=postFormAfterCheck, display='none', submitted="true", postInfo=postJson)

			if postFormAfterCheck.validate_on_submit():
				if postFormAfterCheck.submitAfterCheck.data:
					post = Post(postText=postText, user="2", timestamp=datetime.now(),image=image)
					postDB.session.add(post)
					postDB.session.commit()

					flash("Successfully created a new post!")
					# When the user decides to submit anyway, show the newsfeed.
					#return redirect(urlsConfig.URLS['newsfeed_url'])
					users = json.loads(urllib.request.urlopen(urlsConfig.URLS['allFriends_url']).read())
					print(users)
					postJson = json.dumps({"postText":post.postText,"user":post.user, "friends":users})
					print(postJson)
					return render_template("post.html", title="Post", postForm=postForm, postFormAfterCheck=postFormAfterCheck, display='none', submitted="true", postInfo=postJson)


				elif postFormAfterCheck.discardAfterCheck.data:
					print("Pressed discard")
					# When the user decides to discard post, let him make a new one.
					return redirect(url_for("makePost"))
				else:
					pass

			return render_template("post.html", title="Post", postForm=postForm, postFormAfterCheck=postFormAfterCheck, display='none', submitted="false")
		else:
			return redirect(urlsConfig.URLS['login_url'])
	else:
		return redirect(urlsConfig.URLS['login_url'])

@postApp.route('/makeComment', methods=["GET", "POST"])
def makeComment():
	postID = None
	for key, value in request.form.items():
		if key == "postID":
			postID = value

	# Make call to Comment API
	response = requests.post(urlsConfig.URLS['comment_url'], params={"postID": postID})

	return "OK"

@postApp.route("/getAllPostsForUser/<userId>", methods=["GET"])
def getAllPostsForUser(userId):
	posts = Post.query.filter(Post.user==userId).order_by(desc(Post.timestamp)).all()
	return jsonify([Post.serialize(post) for post in posts])

@postApp.route("/deletePost", methods=['GET', 'POST'])
def deleteUser(id):
    post_id = int(request.args.get('post_id'))
    post = Post.query.filter_by(id=post_id).delete()
    postDB.session.commit()
    return "OK"

# Needed to redirect to urls of another service
@postApp.route("/redirectToGarden", methods=["GET"])
def redirectToGarden():
    global current_user_id

    response = redirect(urlsConfig.URLS['garden_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@postApp.route("/redirectToNewsfeed", methods=["GET"])
def redirectToNewsfeed():
    global current_user_id

    response = redirect(urlsConfig.URLS['newsfeed_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@postApp.route("/redirectToChat",methods=["GET"])
def redirectToChat():
    global current_user_id

    response = redirect(urlsConfig.URLS['chat_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@postApp.route("/redirectToLocation", methods=["GET"])
def redirectToLocation():
    global current_user_id

    response = redirect(urlsConfig.URLS['location_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@postApp.errorhandler(Exception)
def exceptionHandler(error):
	print(error)
	errorString = "Something went wrong! It seems there was a " + error.__class__.__name__ + " while making a request"
	if "profanity" in repr(error).lower():
		errorString += " to the Cyber Bullying service."
	elif "comment" in repr(error).lower():
		errorString += " to the Comment service."
	else:
		errorString += "."
	return errorString