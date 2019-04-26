from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from post import postApp, postDB
from post.forms import PostForm, PostFormAfterCheck
from post.models import Post
from werkzeug.urls import url_parse
import requests
import itertools
import urlsConfig

postText = ""

@postApp.route("/getAllPosts", methods=["GET"])
def getAllPosts():
	posts = Post.query.all()
	return jsonify([Post.serialize(post) for post in posts])

@postApp.route("/post", methods=["GET", "POST"])
def makePost():
	# TODO ask username of current user
	# if current_user.is_authenticated:
	# 	return redirect(url_for("posts"))
	global postText
	
	postForm = PostForm()
	postFormAfterCheck = PostFormAfterCheck()

	if postForm.validate_on_submit():
		postText = postForm.postText.data
		response = requests.post(urlsConfig.URLS['profanity_url'], params={'text': postText})
		# response = requests.post(profanity_url, params={'text': postText})

		# Only show div is post contained a bad word
		if response.text == "BAD":
			return render_template("post.html", title="Post", postForm=postForm, postFormAfterCheck=postFormAfterCheck, display='')
		elif response.text == "GOOD":
			post = Post(postText=postText, user="temp")
			postDB.session.add(post)
			postDB.session.commit()

			flash("Successfully created a new post!")
			return redirect(urlsConfig.URLS['newsfeed_url'])

	if postFormAfterCheck.validate_on_submit():
		if postFormAfterCheck.submitAfterCheck.data:
			post = Post(postText=postText, user="temp")
			postDB.session.add(post)
			postDB.session.commit()

			flash("Successfully created a new post!")
			# When the user decides to submit anyway, show the newsfeed.
			return redirect(urlsConfig.URLS['newsfeed_url'])

		elif postFormAfterCheck.discardAfterCheck.data:
			print("Pressed discard")
			# When the user decides to discard post, let him make a new one.
			return redirect(url_for("makePost"))
		else:
			pass

	return render_template("post.html", title="Post", postForm=postForm, postFormAfterCheck=postFormAfterCheck, display='none')

@postApp.route('/makeComment', methods=["GET", "POST"])
def makeComment():
	postID = None
	for key, value in request.form.items():
		if key == "postID":
			postID = value

	# Make call to Comment API
	response = requests.post(urlsConfig.URLS['comment_url'], params={"postID": postID})

	return "OK"