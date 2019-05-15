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

users = "http://localhost:5001/users/<user_id>"

@app.route("/Admin_User/User/delete/<id>", methods=['GET', 'POST'])
def Admin_User():
    user = User.query.get(id)
    loginDB.session.delete(user)
    loginDB.session.commit()
    return render_template('Admin_User.html', title="User", text=user)

@app.route("/Admin_Comment/Comment/delete/<id>", methods=['GET', 'POST'])
def Admin_Comment():
    comment = Comment.query.get(id)
    commentDB.session.delete(comment)
    commentDB.session.commit()
    return render_template('Admin_Comment.html',title="Comment", text=comment)

@app.route("/Admin_Post/Post/delete/<id>", methods=['GET', 'POST'])
def Admin_Post():
    post = Post.query.get(id)
    postDB.session.delete(post)
    postDB.session.commit()
    return render_template('Admin_Post.html', title="Comment", text=post)

@app.route("/Admin_Photo/Photo/delete/<id>", methods=['GET', 'POST'])
def Admin_Photo():
    photo = Photo.query.get(id)
    photoDB.session.delete(photo)
    photoDB.session.commit()
    return render_template('Admin_Photo.html', title="photo",text=photo)