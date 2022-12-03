from website import create_app
from flask import Flask
from flask_googlemaps import GoogleMaps

# Runs __init__.py in debug mode, this is why when database is messed up, the error message comes up on the webpage.
app = create_app()

# initialize API key for Google Maps API
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBjtiszrLI3QPX3XEJvaITaq_Ns9kFf94Y"

# Inialize extension
GoogleMaps(app, key="AIzaSyBjtiszrLI3QPX3XEJvaITaq_Ns9kFf94Y")

if __name__ == '__main__':
    app.run(debug=True)  # TAKE OUT DEBUG BEFORE PRODUCTION


