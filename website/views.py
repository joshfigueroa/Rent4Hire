from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Note, Item, Location, User
from . import db
import json

views = Blueprint('views', __name__)

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
    if request.form.get('category'):
        category = int(request.form.get('category'))
    else:
        category = 0
    # grab all the items an pass to the webpage
    items = Item.query.all()
    allLocations = []
    for item in items:
        ownerID = item.owner_id
        owner = User.query.get(ownerID)
        locationID = owner.location_id
        ownerLoc = Location.query.get(locationID)
        allLocations.append(str(owner.street) + " " + str(ownerLoc.city) + " " + str(ownerLoc.state) + " " + str(ownerLoc.zip))
    return render_template("home.html", user=user, searched=searched, 
    items=items, location=allLocations, category=category)


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
