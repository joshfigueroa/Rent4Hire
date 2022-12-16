import json
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note, Item, Location, User
from geopy import Nominatim
from geopy.distance import geodesic

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
    # item_coords = []
    # for item in items:
    #     owner_id = item.owner_id
    #     if(owner_id == None):
    #         continue
    #     owner = User.query.get(owner_id)
    #     location_id = owner.location_id
    #     if(location_id == None):
    #         continue
    #     owner_loc = Location.query.get(location_id)
    #     # Need regex for splitting and text removal. Store as a tuple
    #     #get_coordinates(API_KEY, str(owner.street) + " " + str(owner_loc.city) + " " + str(owner_loc.state)
    #     + " " + str(owner_loc.zip))

    #     locator = Nominatim(user_agent="myGeocoder")
    #     address = (str(owner.street) + ", " + str(owner_loc.city) + ", " + str(owner_loc.state) + ", "
    #     + str(owner_loc.zip))
    #     location = locator.geocode(address)
    #     if(location == None):
    #         continue
    #     #print(location.latitude)

    if request.form.get('search'):
        searched = request.form.get('search')
        print(searched)
    else:
        searched = ''
    if request.form.get('radius'):
        search_radius = int(request.form.get('radius'))
    else:
        search_radius = None

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
    # print(all_locations)

    locator = Nominatim(user_agent="myGeocoder")
    user_location_id = current_user.location_id
    user_street = current_user.street
    user_location = Location.query.get(user_location_id)
    user_city = user_location.city
    user_state = user_location.state
    user_zip = user_location.zip

    user_address = str(user_street) + " " + str(user_city) + " " + str(user_state) + " " + str(user_zip)

    curr_addr_geo = locator.geocode(user_address)  # User's current address
    curr_addr_lat_long = (curr_addr_geo.latitude, curr_addr_geo.longitude)  # User's current address lat long

    items_filter_dist = []
    location_filter_list = []
    for locIndex, item in enumerate(items):

        if curr_addr_geo is None:
            continue
        item_addr_geo = locator.geocode(all_locations[locIndex])
        item_addr_lat_long = (item_addr_geo.latitude, item_addr_geo.longitude)  # Current item's lat long
        distance = geodesic(curr_addr_lat_long, item_addr_lat_long).miles
        if search_radius is None or search_radius == 0 or search_radius > distance:
            items_filter_dist.append(item)
            location_filter_list.append(all_locations[locIndex])

    return render_template("home.html", user=user, searched=searched,
                           items=items_filter_dist, location=location_filter_list, category=category,
                           search_radius=search_radius)


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
