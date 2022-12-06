from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from .models import Note, Item, Location
from . import db
import json
import os

views = Blueprint('views', __name__)

# Defines allowed filetypes for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Defines proper filename for upload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes to the home page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home(): 
    user=current_user
    location=Location.query.get(user.location_id)
    # if there has been a search request, pass it through searched. else pass ''
    if request.form.get('search'):
        searched = request.form.get('search')
        print(searched) 
    else:
        searched = ''
    category = int(request.form.get('category'))
    #category = 0
    print(category)
    # grab all the items an pass to the webpage
    items = Item.query.all()
    return render_template("home.html", user=user, searched=searched, 
    items=items, location=location, category=category)

# !!!!!!!!!WHAT EVEN IS ALL OF THIS?!!!!!!!!!
@views.route('/', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

#!!!!!!!!!!!!!WHATS THIS FOR???!!!!!!!!!!!!!!
@views.route('/display/<filename>')
@login_required
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


# This would be good to update to delete rental listing or something like that/ maybe even useful for deleting user
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# Route to a testing page, test whatever html/css you want to play with
@views.route('/test')
@login_required
def test_every():
    return render_template("test.html", user=current_user)
