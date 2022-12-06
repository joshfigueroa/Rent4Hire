from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Location
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_googlemaps import GoogleMaps, Map, get_address, get_coordinates

auth = Blueprint('auth', __name__)


# Route of what happens to input on login page, checks if email exists then if input = password, make current user
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password or email, try again.', category='error')
        else:
            flash('Incorrect password or email, try again.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Todo: Update with optional location fields/number
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        street = request.form.get('street')
        # Adding city, state, and zip to location. 
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        user = User.query.filter_by(email=email).first()
        location = Location.query.filter_by(city=city, state=state, zip=zip_code).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')  # CHECK THIS
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')

        # !!!!!!!! TO DO: ERROR CHECKING, CLEAN UP!!!!!!!!!!!!
        elif len(city) < 1:
            flash('Enter city name.', category='error')
        elif len(state) < 1:
            flash('Enter state name.', category='error')
        elif len(zip_code) > 5 or len(zip_code) < 5:
            flash('Invalid zip code.', category='error')
        # If city, state, zip exists in table, get id            
        elif location:
            # Create user with location id
            new_user = User(email=email, first_name=first_name, last_name=last_name, street=street,
                            location_id=location.id, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        else:
            # If not in table, create location,
            # grab location id and add create user with location
            new_location = Location(city=city, state=state, zip=zip_code)
            db.session.add(new_location)
            db.session.commit()
            # location = Location.query.filter_by(city=city, state=state, zip=zip_code).first()
            new_user = User(email=email, first_name=first_name, last_name=last_name, street=street,
            location_id=location.id, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! New location', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
