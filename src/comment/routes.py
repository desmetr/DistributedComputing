from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from comment import commentApp, commentDB
from comment.forms import CommentForm, CommentFormAfterCheck
from comment.models import Comment
from werkzeug.urls import url_parse
from sqlalchemy import desc
from datetime import datetime
import requests
import urlsConfig

commentText = ""
postID = None

@commentApp.route("/comment", methods=["GET", "POST"])
def comment():
	global postID, commentText

	commentForm = CommentForm()
	commentFormAfterCheck = CommentFormAfterCheck()

	# We come here twice, from different forms, only use it once.
	if 'postID' in request.form:
		postID = request.form['postID']

	if commentForm.validate_on_submit():
		commentText = commentForm.commentText.data
		response = requests.post(urlsConfig.URLS['profanity_url'], params={'text': commentText})

		# Only show div is post contained a bad word
		if response.text == "BAD":
			return render_template("comment.html", title="Comment", commentForm=commentForm, commentFormAfterCheck=commentFormAfterCheck, display='')
		elif response.text == "GOOD":
			comment = Comment(commentText=commentText, user="temp", postID=postID, timestamp=datetime.now())
			commentDB.session.add(comment)
			commentDB.session.commit()

			print("Successfully placed a comment!")
			return redirect(urlsConfig.URLS['newsfeed_url'])

	if commentFormAfterCheck.validate_on_submit():
		if commentFormAfterCheck.submitAfterCheck.data:
			comment = Comment(commentText=commentText, user="temp", postID=postID, timestamp=datetime.now())
			commentDB.session.add(comment)
			commentDB.session.commit()

			flash("Successfully created a new comment!")
			return redirect(urlsConfig.URLS['newsfeed_url'])

		elif commentFormAfterCheck.discardAfterCheck.data:
			print("Pressed discard")
			return redirect(url_for("comment"))
		else:
			pass

	return render_template("comment.html", title="Comment", commentForm=commentForm, commentFormAfterCheck=commentFormAfterCheck, display='none')

@commentApp.route("/getCommentsOnePost", methods=["GET"])
def getCommentsOfPost():
	postID = request.args.get('postID')

	comments = Comment.query.filter_by(postID=int(postID)).all()
	return jsonify([Comment.serialize(comment) for comment in comments])

@commentApp.route("/getCommentsAllPosts", methods=["GET"])
def getCommentsOfAllPosts():
	# comments = Comment.query.all()
	comments = Comment.query.order_by(desc(Comment.timestamp)).all()
	return jsonify([Comment.serialize(comment) for comment in comments])