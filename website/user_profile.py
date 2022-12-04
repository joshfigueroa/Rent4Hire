from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, Location, Item, Category
from . import db


user_profile = Blueprint('user_profile', __name__)

# Need for updates?
# Routes to create rental profile
@user_profile.route('/rental_profile', methods=['GET', 'POST'])
@login_required
def rental_profile():
    user=current_user
    location=Location.query.get(user.location_id)
    if request.method == 'POST':
        if request.form.get('submit_button') == "Submit":
            pass
        if request.form.get('chat_button') == "Chat":
            return render_template('chat.html', user=user)
    return render_template("rental_profile.html", user=user)


@user_profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    check_auth = False
    user = current_user
    location=Location.query.get(user.location_id)
    if request.method == 'POST':        
        if check_auth:
            print("here")
            if request.form['submit'] == 'submitNewInfo':
                first_name = request.form.get('firstName')
                last_name = request.form.get('lastName')
                email = request.form.get('email')
                street = request.form.get('street')
                city = request.form.get('city')
                state = request.form.get('state')
                zip_code = request.form.get('zip')
                
                update_user = User.query.filter_by(id=user.id).first()
                
                # If first name is entered, 
                if len(first_name) > 0:
                    # Check to see if input is more than 1 character
                    if len(first_name) < 2:
                        flash('First name must be greater than 1 character.', category='error')
                    else:
                        # Update firstname in db
                        user.first_name = first_name
                        db.session.commit()
                        flash("Profile Updated!", category='success')
                        
                # If last name is entered, 
                if len(last_name) > 0:
                    # Check to see if input is more than 1 character
                    if len(last_name) < 2:
                        flash('Last name must be greater than 1 character.', category='error')
                    else:
                        # Update lastname in db
                        user.last_name = last_name
                        db.session.commit()
                        flash("Profile Updated!", category='success')
                
                # If email is entered,
                if len(email) > 0:
                    # Check to see if email exists
                    if User.query.filter_by(email=email).first():
                        flash('Email already exists.', category='error')
                    elif len(email) < 4:
                        flash('Email must be greater than 3 characters.', category='error')
                    else:
                        # Update email in db
                        user.email = email
                        db.session.commit()
                        flash("Profile Updated!", category='success')
                
                # If street is entered,
                if len(street) > 0:
                    # check if more than 1 character
                    if len(street) < 2:
                        flash('Street addess must be greater than 1 character.', category='error')
                    else:
                        # Update street address in db
                        user.street = street
                        db.session.commit()
                        flash("Profile Updated!", category='success')
                
                # If one of city/state/zip has input
                if (len(city) > 0) or (len(state) > 0) or (len(zip_code) > 0):
                    # and all city/state/zip has input
                    if (len(city) > 0) and (len(state) > 0) and (len(zip_code) > 0):
                        location = Location.query.filter_by(city=city, state=state, zip=zip_code).first()
                        # If location exists, update user location id
                        if location:
                            user.location_id = location.id
                            db.session.commit()
                            flash("Profile Updated!", category='success')
                        else:
                            # If valid zipcode,
                            if len(zip_code) == 5:
                                # Add new location to location table
                                new_location = Location(city=city, state=state, zip=zip_code)
                                db.session.add(new_location)
                                # Update location in db
                                user.location_id = new_location.id
                                db.session.commit()
                                flash("Profile Updated!", category='success')
                            else:
                                flash('Not a valid zipcode', category='error')          
                    # Not all city/state/zip has input
                    else:
                        flash('One of city/state/zip is not entered', category='error')
                        
            elif request.form['submit'] == 'Submit New Password':
                update_user = User.query.filter_by(email=user.email).first()
                new_password = request.form.get('newPassword')
                conf_password = request.form.get('confPassword')
                if new_password == conf_password:
                    update_user.password = generate_password_hash(new_password, method='sha256')
                    db.session.commit()
                    flash("Password Updated!", category='success')
                else:
                    flash("Passwords don't match.", category='error')
        
        check_password = request.form.get('password')
        if check_password_hash(user.password, check_password):
            check_auth = True
        else:
            check_auth = False
            flash("Incorrect credentials, try again.", category='error')
    
    return render_template("profile_dash.html", user=user, checkAuth=check_auth, location=location)

# page for individual items. gets passed the item id, returns the object.
@user_profile.route('/item/<id>', methods=['GET', 'POST'] )
@login_required
def display_item(id):
    # Creates date/time form
    currentItem=Item.query.get(id)
    category=Category.query.get(currentItem.category_id)
    
    return render_template('item.html', user=current_user, currentItem=currentItem,
                           category=category)
 