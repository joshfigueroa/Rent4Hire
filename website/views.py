from flask import Blueprint, Flask, render_template, request, flash, jsonify, redirect, url_for, app
from flask_login import login_required, current_user
from flask_googlemaps import GoogleMaps, Map
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm

from .models import Note, User, Item, Category
from . import db
import json
import os

views = Blueprint('views', __name__)

# Defines allowed filetypes for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Defines proper filename for upload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes to the home page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home(): 
    # if there has been a search request, pass it through searched. else pass ''
    if request.form.get('search'):
        searched = request.form.get('search')
    else:
        searched = ''
    # grab all the items an pass to the webpage
    items = Item.query.all()
    return render_template("home.html", user=current_user, searched=searched, 
    items=items)


@views.route('/', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

#!!!!!!!!!!!!!WHATS THIS FOR???!!!!!!!!!!!!!!
@views.route('/display/<filename>')
@login_required
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


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

# page for individual items. gets passed the item id, returns the object.
@views.route('/item/<id>', methods=['GET', 'POST'] )
@login_required
def display_item(id):
    if request.method == 'POST':
        if request.form.get('submit_button') == "Submit":
            pass
        if request.form.get('chat_button') == "Chat":
            return render_template('chat.html', user=current_user)
        # NEED TO DISPLAY CATEGORY NAME ASSIGNED TO ITEM
    return render_template('item.html', user=current_user, currentItem=Item.query.get(id),
                           category=Category.query.all())

# Convert dollars to cents to store nicely in database
def convertToCents(dollars):
    cents=int(dollars)*100
    return cents

# Routes to create listing page
@views.route('/create', methods=['GET', 'POST'])
@login_required
def create_listing():  # CHANGE NAME
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        description = description.strip() # Trim white spcae at each end
        # item_location_id = Column(Integer)#, ForeignKey("locations.id"), index=True) #Not sure if this is needed
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        value = request.form.get('value')
        
        #item = Item.query.filter_by(name=name).first() #idk if needed to filter something first
        
        # ERROR CHECKING
        if len(name) < 1:
            flash('Name is too short', category='error')
        elif len(name) > 254:
            flash('Name max character count is 255', category='error')
        elif len(description) < 1:
            flash('Insert descripton', category='error')  
        elif quantity == None:
            flash('Select a quantity', category='error')
        elif price == None:
            flash('Input price', category='error')
        elif value == None:
            flash('Input value', category='error')
        else:
            # NEED TO ADD PICTURE INFO LATER!!!!!!!!!!!!
            
            # Convert string to integer
            #category=int(categoryStr)
            
            # Convert dollars to cents
            price_in_cents=convertToCents(price)
            value_in_cents=convertToCents(value)
        
            new_item = Item(name=name, category_id=category, 
                            description=description, owner_id=current_user.id,
                            price_in_cents=price_in_cents, quantity=quantity,
                            value_in_cents=value_in_cents)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_listing.html", user=current_user)

# SHOULD BE ABLE TO DELETE!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Routes to create rental profile
@views.route('/rental_profile', methods=['GET', 'POST'])
@login_required
def rental_profile():
    if request.method == 'POST':
        if request.form.get('submit_button') == "Submit":
            pass
        if request.form.get('chat_button') == "Chat":
            return render_template('chat.html', user=current_user)
    return render_template("rental_profile.html", user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    check_auth = False
    user = current_user
    if request.method == 'POST':
        if check_auth:
            print("here")
            if request.form['submit'] == 'submitNewInfo':
                user_db = User.query.filter_by(email=user.email).first()
                user_db.first_name = request.form.get('firstName')
                user_db.last_name = request.form.get('lastName')
                user_db.email = request.form.get('email')
                user_db.street = request.form.get('street')
                db.session.commit()
                flash("Profile Updated!", category='success')
            elif request.form['submit'] == 'Submit New Password':
                user_db = User.query.filter_by(email=user.email).first()
                new_password = request.form.get('password')
                conf_password = request.form.get('confPassword')
                if new_password == conf_password:
                    user_db.password = generate_password_hash(new_password, method='sha256')
                    db.session.commit()
                    flash("Password Updated!", category='success')
                else:
                    flash("Passwords don't match.", category='error')
        print("here 2")
        check_password = request.form.get('password')
        if check_password_hash(user.password, check_password):
            check_auth = True
        else:
            check_auth = False
            flash("Incorrect credentials, try again.", category='error')
        return render_template("profile_dash.html", user=user, checkAuth=check_auth)
    elif request.method == 'GET':
        return render_template("profile_dash.html", user=user, checkAuth=check_auth)


# Route to a testing page, test whatever html/css you want to play with
@views.route('/test')
@login_required
def test_every():
    return render_template("test.html", user=current_user)

# Route to a testing page for maps
@views.route('/maptest')
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
