from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from post import postApp, postDB
from post.forms import PostForm
from post.models import Post
from werkzeug.urls import url_parse

@postApp.route("/", methods=["GET"])
@postApp.route("/index", methods=["GET"])
def index():
	posts = Post.query.all()
	return render_template("index.html", title="Home", posts=posts)

@postApp.route("/post", methods=["GET", "POST"])
def makePost():
	# if current_user.is_authenticated:
	# 	return redirect(url_for("index"))
	
	form = PostForm()
	if form.validate_on_submit():
		# TODO ask username of current user
		post = Post(postText=form.postText.data, user="temp")
		postDB.session.add(post)
		postDB.session.commit()

		flash("Successfully created a new post!")
		return redirect(url_for("index"))

	return render_template("post.html", title="Post", form=form)