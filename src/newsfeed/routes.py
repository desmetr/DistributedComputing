from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from newsfeed import newsfeedApp
from werkzeug.urls import url_parse
from comment.forms import CommentForm
import requests
import random
import urlsConfig

@newsfeedApp.route("/newsfeed", methods=["GET"])
def newsfeed():
	# Get all posts
	allPosts = requests.get(urlsConfig.URLS['all_posts_url']).json()
	# allPosts = []

	# Get all comments
	allComments = requests.get(urlsConfig.URLS['all_comments_all_posts_url']).json()
	# allComments = []

	# Get all photos
	# allPhotos = requests.get(urlsConfig.URLS['all_photos_url']).json()
	allPhotos = []

	# Get all advertisements
	advertisements = []

	commentForm = CommentForm()

	# Show list
	return render_template("newsfeed.html", commentForm=commentForm, posts=allPosts, comments=allComments, photos=allPhotos, advertisements=advertisements)