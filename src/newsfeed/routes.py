from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from newsfeed import newsfeedApp
from werkzeug.urls import url_parse
from comment.forms import CommentForm
import requests
import urlsConfig

@newsfeedApp.route("/newsfeed", methods=["GET"])
def newsfeed():
	current_user_id = request.cookies.get("currentSessionCookie")
	if current_user_id:
		# Get current user information
		current_user_response = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id))
		if current_user_response.status_code == 200:
			# Success!

			# Get all posts ---> THIS IS IN COMMENT JUST TO TEST OTHER STUFF, THIS IS THE CORRECT CODE
			# allPosts = requests.get(urlsConfig.URLS['all_posts_url']).json()
			allPosts = []

			# Get all comments
			# allComments = requests.get(urlsConfig.URLS['all_comments_all_posts_url']).json()
			allComments = []

			# Get all photos
			# allPhotos = requests.get(urlsConfig.URLS['all_photos_url']).text
			allPhotos = []

			# Get all advertisements
			# allAdvertisements = requests.get(urlsConfig.URLS['advertisements_url'])
			# print(allAdvertisements)
			allAdvertisements = []

			commentForm = CommentForm()

			# Show list
			return render_template("newsfeed.html", commentForm=commentForm, posts=allPosts, comments=allComments, photos=allPhotos, advertisements=allAdvertisements)
		else:
			return redirect(urlsConfig.URLS['login_url'])
	else:
		return redirect(urlsConfig.URLS['login_url'])

@newsfeedApp.errorhandler(Exception)
def exceptionHandler(error):
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
