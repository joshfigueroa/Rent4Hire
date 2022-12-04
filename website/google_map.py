from flask import Blueprint, render_template
from flask_login import login_required

from flask_googlemaps import Map

google_map = Blueprint('google_map', __name__)

# Route to a testing page for maps
@google_map.route('/maptest')
@login_required
def test_map():
    test_map = Map(
                identifier="view-side",
                varname="test_map",
                style="height:720px;width:1100px;margin:0;", # hardcoded!
                lat=37.4419, # hardcoded!
                lng=-122.1419, # hardcoded!
                zoom=15,
                markers=[(37.4419, -122.1419)] # hardcoded!
            )
    return render_template('example_test_map.html', test_map=test_map) 
