from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from comment import commentApp, commentDB
from comment.forms import CommentForm
from comment.models import Comment
from werkzeug.urls import url_parse
import requests

@commentApp.route("/comment", methods=["GET", "POST"])
def comment():
	print("in comment")
	commentForm = CommentForm()

	if commentForm.validate_on_submit():
		postID = request.args.get('postID')
		postID = 2
		commentText = commentForm.commentText.data

		comment = Comment(commentText=commentText, user="temp", postID=postID)
		commentDB.session.add(comment)
		commentDB.session.commit()

		flash("Successfully placed a comment!")
		return 'OK'

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