from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from comment import commentApp, commentDB
from comment.forms import CommentForm
from comment.models import Comment
from werkzeug.urls import url_parse
import requests

postID = None

@commentApp.route("/comment", methods=["GET", "POST"])
def comment():
	global postID

	commentForm = CommentForm()

	# We come here twice, from different forms, only use it once.
	if 'postID' in request.form:
		postID = request.form['postID']

	if commentForm.validate_on_submit():
		commentText = commentForm.commentText.data

		comment = Comment(commentText=commentText, user="temp", postID=postID)
		commentDB.session.add(comment)
		commentDB.session.commit()

		print("Successfully placed a comment!")
		return render_template("commentSuccess.html", title="Comment Success")

	return render_template("comment.html", title="Comment", commentForm=commentForm)

@commentApp.route("/getCommentsOnePost", methods=["GET"])
def getCommentsOfPost():
	postID = request.args.get('postID')

	comments = Comment.query.filter_by(postID=int(postID)).all()
	return jsonify([Comment.serialize(comment) for comment in comments])

@commentApp.route("/getCommentsAllPosts", methods=["GET"])
def getCommentsOfAllPosts():
	comments = Comment.query.all()
	return jsonify([Comment.serialize(comment) for comment in comments])