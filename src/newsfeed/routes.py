from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from newsfeed import newsfeedApp
from werkzeug.urls import url_parse
import requests
import random

all_posts_url = "http://localhost:5000/getAllPosts"
all_comments_all_posts_url = "http://localhost:5001/getCommentsAllPosts"

@newsfeedApp.route("/newsfeed", methods=["GET"])
def newsfeed():
	# Get all posts
	allPosts = requests.get(all_posts_url).json()

	# Get all comments
	allComments = requests.get(all_comments_all_posts_url).json()

	# # Link post with correct comments
	# postsAndComments = {}
	# for post in allPosts:
	# 	print(post)
	# 	postsAndComments[post] = []
	# for post in allPosts:
	# 	for comment in allComments:
	# 		if comment['postID'] == post['id']:
	# 			postsAndComments[post].append(comment)
	# 			# if post in postsAndComments:
	# 			# else:
	# 			# 	postsAndComments[post] = [comment]

	# print(postsAndComments)
	# Get all advertisements
	advertisements = []

	# Show list
	return render_template("newsfeed.html", posts=allPosts, comments=allComments, advertisements=advertisements)