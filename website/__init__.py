from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path

db = SQLAlchemy()
DB_NAME = "instance/database.db"
DB_PATH = Path(DB_NAME).resolve()

UPLOAD_FOLDER = 'website\static\images'
UPLOAD_PATH = Path(UPLOAD_FOLDER).resolve()

def create_app():
    app = Flask(__name__, static_url_path='/static') # static_url_path in order to init path for anything in static folder
    app.config['SECRET_KEY'] = 'ireuhgkdjfndlfkgjdslhjlkjgjvcbbjh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///' + str(DB_PATH)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False      # HOPING TO FIX issue with db at start up -> DIDNT WORK
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db.init_app(app)

    from .views import views
    from .auth import auth

    # Makes files with routes blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    # Creates an empty database
    # with app.app_context():
    #    db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app
