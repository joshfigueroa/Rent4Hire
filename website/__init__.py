from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, static_url_path='/static') # static_url_path in order to init path for anything in static folder
    app.config['SECRET_KEY'] = 'ireuhgkdjfndlfkgjdslhjlkjgjvcbbjh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///' + DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True      # HOPING TO FIX issue with db at start up -> DIDNT WORK
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
        return User.query.get(int(id))

    return app
