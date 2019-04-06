from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, IMAGES
from photo import photoApp, photoDB
from photo.forms import PhotoForm
from photo.models import Photo
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
photos = UploadSet('photos', IMAGES)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@photoApp.route('/photo')
def photo():
	form = PhotoForm()
	return render_template('upload.html', title='Photo', form=form)

@photoApp.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST' and 'inputFile' in request.files:
		upload = request.files['inputFile']

		# We save the relative path to the static folder, absolute paths didn't work in showing of photo.
		uploadURL = os.path.join(UPLOAD_FOLDER, upload.filename)
		upload.save(uploadURL)

		newPhoto = Photo(url=uploadURL, filename=upload.filename, user='temp')
		photoDB.session.add(newPhoto)
		photoDB.session.commit()

		flash('Succesfully uploaded a new photo!')
		return redirect(url_for('showOnePhoto', id=newPhoto.id))
	return render_template('upload.html')

@photoApp.route('/photo/<id>')
def showOnePhoto(id):
	photo = Photo.query.filter_by(id=id).first()
	return render_template('photo.html', filename=photo.filename)

@photoApp.route('/photo/all')
def showAllPhotos():
	photos = Photo.query.all()
	return jsonify([Photo.serialize(photo) for photo in photos])