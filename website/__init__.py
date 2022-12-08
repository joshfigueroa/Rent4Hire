from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path
from flask_googlemaps import GoogleMaps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os

db = SQLAlchemy()
DB_NAME = "instance/database.db"
DB_PATH = Path(DB_NAME).resolve()


def set_destination(app):
    return os.path.join(app.instance_path, "images")

photos = UploadSet(name='photos', extensions=IMAGES, default_dest=set_destination)

def create_app():
    app = Flask(__name__,
                static_url_path='/static')  # static_url_path in order to init path for anything in static folder
    app.config['SECRET_KEY'] = 'ireuhgkdjfndlfkgjdslhjlkjgjvcbbjh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///' + str(DB_PATH)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # HOPING TO FIX issue with db at start up -> DIDNT WORK
    
    
    # initialize API key for Google Maps API
    app.config['GOOGLEMAPS_KEY'] = "AIzaSyBjtiszrLI3QPX3XEJvaITaq_Ns9kFf94Y"
    # Inialize extension
    GoogleMaps(app, key="AIzaSyBjtiszrLI3QPX3XEJvaITaq_Ns9kFf94Y")

    # Fileupload config
    app.config["UPLOADED_PHOTOS_DEST"] = "website/static/images"
    configure_uploads(app, photos)

    db.init_app(app)

    from .views         import views    #This has code thats not in use
    from .auth          import auth
    from .order_item    import order_item
    from .google_map    import google_map
    from .create_item   import create_item
    from .user_profile  import user_profile #Some code not in use
    from .edit_item  import edit_item

    # Makes files with routes blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(order_item, url_prefix='/')
    app.register_blueprint(google_map, url_prefix='/') # Did not test blueprint
    app.register_blueprint(create_item, url_prefix='/')
    app.register_blueprint(edit_item, url_prefix='/')
    app.register_blueprint(user_profile, url_prefix='/')
    
    
    
    from .models import User

    # Creates an empty database
    if DB_PATH.exists() == False:
        with app.app_context():
            db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
