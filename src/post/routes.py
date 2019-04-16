from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from post import postApp, postDB
from post.forms import PostForm, PostFormAfterCheck
from post.models import Post
from werkzeug.urls import url_parse
import requests

profanity_url = "http://localhost:5001/profanity" 
postText = ""

@postApp.route("/posts", methods=["GET"])
def posts():
	posts = Post.query.all()
	return render_template("posts.html", title="Home", posts=posts)

@postApp.route("/post", methods=["GET", "POST"])
def makePost():
	# if current_user.is_authenticated:
	# 	return redirect(url_for("posts"))
	global postText
	
	postForm = PostForm()
	postFormAfterCheck = PostFormAfterCheck()

	if postForm.validate_on_submit():
		postText = postForm.postText.data
		response = requests.post(profanity_url, params={'text': postText})

		# Only show div is post contained a bad word
		if response.text == "BAD":
			return render_template("post.html", title="Post", postForm=postForm, postFormAfterCheck=postFormAfterCheck, display='')
		elif response.text == "GOOD":
			post = Post(postText=postText, user="temp")
			postDB.session.add(post)
			postDB.session.commit()

			flash("Successfully created a new post!")
			return redirect(url_for("posts"))

	if postFormAfterCheck.validate_on_submit():
		if postFormAfterCheck.submitAfterCheck.data:
			# TODO ask username of current user
			# post = Post(postText=postFormAfterCheck.postText.data, user="temp")
			post = Post(postText=postText, user="temp")
			postDB.session.add(post)
			postDB.session.commit()

			flash("Successfully created a new post!")
			return redirect(url_for("posts"))

		elif postFormAfterCheck.discardAfterCheck.data:
			print("Pressed discard")
			return redirect(url_for("makePost"))
			# return redirect(url_for("posts"))
		else:
			pass

	return render_template("post.html", title="Post", postForm=postForm, postFormAfterCheck=postFormAfterCheck, display='none')