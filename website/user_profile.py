from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, Location, Item, Category, Order
from . import db
import datetime
import math 


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

check_auth=False
@user_profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    global check_auth
    user = current_user
    location=Location.query.get(user.location_id)

    listItem = []
    listItemUser = []
    listUserLocation = []
    print(listItem)

    for oneOrder in user.orders:
        orderItem = Item.query.get(oneOrder.item_id)
        itemUser = User.query.get(orderItem.owner_id)
        userLocation = Location.query.get(itemUser.location_id)
        listItem.append(orderItem)
        listItemUser.append(itemUser)
        listUserLocation.append(userLocation)

    if request.method == 'POST':   
        updated = 1
        if check_auth:
            if request.form.get('submitNewInfo') == 'Update Profile':
                
                first_name = request.form.get('firstName')
                last_name = request.form.get('lastName')
                email = request.form.get('email')
                street = request.form.get('street')
                city = request.form.get('city')
                state = request.form.get('state')
                zip_code = request.form.get('zip')
                
                # If first name is entered, 
                if len(first_name) > 0:
                    # Check to see if input is more than 1 character
                    if len(first_name) < 2:
                        flash('First name must be greater than 1 character.', category='error')
                    else:
                        # Update firstname in db
                        user.first_name = first_name
                        db.session.commit()
                        updated = 0
                        
                # If last name is entered, 
                if len(last_name) > 0:
                    # Check to see if input is more than 1 character
                    if len(last_name) < 2:
                        flash('Last name must be greater than 1 character.', category='error')
                    else:
                        # Update lastname in db
                        user.last_name = last_name
                        db.session.commit()
                        updated = 0
                
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
                        updated = 0
                
                # If street is entered,
                if len(street) > 0:
                    # check if more than 1 character
                    if len(street) < 2:
                        flash('Street addess must be greater than 1 character.', category='error')
                    else:
                        # Update street address in db
                        user.street = street
                        db.session.commit()
                        updated = 0
                
                # If one of city/state/zip has input
                if (len(city) > 0) or (len(state) > 0) or (len(zip_code) > 0):
                    # and all city/state/zip has input
                    if (len(city) > 0) and (len(state) > 0) and (len(zip_code) > 0):
                        print('hello')
                        location = Location.query.filter_by(city=city, state=state, zip=zip_code).first()

                        # If location exists, update user location id
                        if location:
                            
                            user.location_id = location.id
                            db.session.commit()
                            updated = 0
                        else:
                            # If valid zipcode,
                            if len(zip_code) == 5:
                                # Add new location to location table
                                new_location = Location(city=city, state=state, zip=zip_code)
                                db.session.add(new_location)
                                db.session.commit()
                                # Update location in db
                                user.location_id = new_location.id
                                db.session.commit()
                                updated = 0
                                
                            else:
                                flash('Not a valid zipcode', category='error')          
                    # Not all city/state/zip has input
                    else:
                        flash('One of city/state/zip is not entered', category='error')
                
                new_password = request.form.get('newPassword')
                print(new_password)
                conf_password = request.form.get('confPassword')
                print(new_password)
                if new_password != '':
                    if new_password == conf_password:
                        if len(new_password) < 7:
                            flash('Password must be at least 7 characters.', category='error')
                        user.password = generate_password_hash(new_password, method='sha256')
                        db.session.commit()
                        flash("Password Updated!", category='success')
                    else:
                        flash("Passwords don't match.", category='error')


            if request.form.get('SubmitNewPassword') == "Change Password":
                new_password = request.form.get('newPassword')
                conf_password = request.form.get('confPassword')
                print(new_password)
                if new_password == conf_password:
                    if len(new_password) < 7:
                        flash('Password must be at least 7 characters.', category='error')
                    user.password = generate_password_hash(new_password, method='sha256')
                    db.session.commit()
                    flash("Password Updated!", category='success')
                else:
                    flash("Passwords don't match.", category='error')
        if updated == 0:
            flash("Profile Updated!", category='success')

        
        
        if not check_auth:
            print("in not auth")
            if request.form.get('submit'):
                check_password = request.form.get('password')
                if check_password_hash(user.password, check_password):
                    check_auth = True
                else:
                    check_auth = False
                    flash("Incorrect credentials, try again.", category='error')
            
    return render_template("profile_dash.html", user=user, checkAuth=check_auth, location=location, listItem =listItem, listItemUser=listItemUser, listUserLocation=listUserLocation)

# Routing for pickup
@user_profile.route('/pickup/item/<id>')
@login_required
def pickup_order(id):
    currentOrder = Order.query.get(id)
    currentOrder.actual_pickup_date = datetime.datetime.now()
    db.session.commit()
    flash("You have successfully picked up the order!", category='success')

    return redirect(url_for('user_profile.profile_page'))

# Routing for return
@user_profile.route('/return/item/<id>')
@login_required
def return_order(id):
    currentOrder = Order.query.get(id)
    print(currentOrder)
    currentItem = Item.query.get(currentOrder.item_id)
    print(currentItem)
    currentOrder.actual_return_date = datetime.datetime.now()
    currentOrder.total = currentOrder.quantity * (currentItem.price_in_cents * math.ceil((currentOrder.actual_return_date-currentOrder.actual_pickup_date).days+1))
    
    db.session.commit()

    if currentOrder:
        currentItem.is_available = True
        currentOrder.is_active = False
        message = f"You have successfully returned the order! Now you have to pay {currentOrder.total/100}0"
        flash(message, category='success')
        db.session.commit()

    return redirect(url_for('user_profile.profile_page'))

# page for individual items. gets passed the item id, returns the object.
@user_profile.route('/item/<id>', methods=['GET', 'POST'] )
@login_required
def display_item(id):
    # Creates date/time form
    currentItem=Item.query.get(id)
    category=Category.query.get(currentItem.category_id)
    
    return render_template('item.html', user=current_user, currentItem=currentItem,
                           category=category)
 

@user_profile.route('/history/<id>')
@login_required
def item_history(id):
    listOrder = []
    listRenter = []
    listRenterLocation = []
    currentItem = Item.query.get(id)
    for order in currentItem.orders:
        renterUser = User.query.get(order.renter_id)
        renterLocation = Location.query.get(renterUser.location_id)
        listOrder.append(order)
        listRenter.append(renterUser)
        listRenterLocation.append(renterLocation)
    return render_template('item_history.html', user=current_user, currentItem=currentItem, listOrder=listOrder, listRenter=listRenter, listRenterLocation=listRenterLocation)