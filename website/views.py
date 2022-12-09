import json
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note, Item, Location, User
from flask import Flask
from geopy import Nominatim

views = Blueprint('views', __name__)


# Routes to the home page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user = current_user
    # location = Location.query.get(user.location_id)
    # if there has been a search request, pass it through searched. else pass ''
    items = Item.query.all()
    # grab all the items an pass to the webpage
    # list of tuples
    item_coords = []
    for item in items:
        owner_id = item.owner_id
        if(owner_id == None):
            continue
        owner = User.query.get(owner_id)
        location_id = owner.location_id
        if(location_id == None):
            continue
        owner_loc = Location.query.get(location_id)
        # Need regex for splitting and text removal. Store as a tuple
        #get_coordinates(API_KEY, str(owner.street) + " " + str(owner_loc.city) + " " + str(owner_loc.state) + " " + str(owner_loc.zip))

        locator = Nominatim(user_agent="myGeocoder")
        address = (str(owner.street) + ", " + str(owner_loc.city) + ", " + str(owner_loc.state) + ", " + str(owner_loc.zip))
        location = locator.geocode(address)
        if(location == None):
            continue
        print(location.latitude)

    if request.form.get('search'):
        searched = request.form.get('search')
        print(searched)
    else:
        searched = ''
    if request.form.get('radius'):
        search_radius = request.form.get('radius')

        print(search_radius)
    if request.form.get('category'):
        category = int(request.form.get('category'))
    else:
        category = 0
    # grab all the items an pass to the webpage
    all_locations = []
    for item in items:
        owner_id = item.owner_id
        owner = User.query.get(owner_id)
        location_id = owner.location_id
        owner_loc = Location.query.get(location_id)
        all_locations.append(
            str(owner.street) + " " + str(owner_loc.city) + " " + str(owner_loc.state) + " " + str(owner_loc.zip))
    return render_template("home.html", user=user, searched=searched,
                           items=items, location=all_locations, category=category)


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
