from Admin import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
# from __init__ import loginApp, loginDB
from login import loginApp, loginDB
from login.models import User, loginDB
from comment.models import Comment, commentDB
from post.models import Post, postDB
from photo.models import Photo, photoDB
from werkzeug.urls import url_parse
import urlsConfig

users = "http://localhost:5001/users/<user_id>"

@app.route("/admin", methods=['GET'])
def admin():
    users = requests.get(urlsConfig.URLS['users_url'])
    comments = requests.get(urlsConfig.URLS['comment_url'])
    posts = requests.get(urlsConfig.URLS['all_posts_url'])
    advertisements = requests.get(urlsConfig.URLS['advertisements_url'])

    return render_template("admin.html",users=users, comments=comments, posts=posts, advertisements=advertisements )

@app.route("/delete/<id>", methods=['GET', 'POST'])
def deleteUser(id):
    if 'userID' in request.form:
        userID = request.form['userID']
        response = requests.get(urlsConfig.URLS['delete_user'] + str(userID))
        return redirect('admin')

@app.route("/delete/<id>", methods=['GET', 'POST'])
def deleteComment():
    if 'commentID' in request.form:
        commentID = request.form['commentID']
        response= requests.get(urlsConfig.URLS['delete_comment'] + str(commentID))
    return redirect('admin')

@app.route("/delete/<id>", methods=['GET', 'POST'])
def deletePost():
    if 'postID' in request.form:
        postID = request.form['postID']
        response= requests.get(urlsConfig.URLS['delete_post'] +  str(postID))
    return redirect('admin')

@app.route("/delete/<id>", methods=['GET', 'POST'])
def deleteAdverstiment():
    if 'advertisingID' in request.form:
        advertisingID = request.form['advertisingID']
        response= requests.get(urlsConfig.URLS['advertising_post'] +  str(advertisingID))
    return redirect('admin')