from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Item
from . import db
from . import __init__
from pathlib import Path
from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, configure_uploads, IMAGES

UPLOAD_FOLDER = 'website\\static\\images'
UPLOAD_PATH = Path(UPLOAD_FOLDER).resolve()

photos = UploadSet("photos", IMAGES)

edit_item = Blueprint('edit_item', __name__)

# Convert dollars to cents to store nicely in database
def convertToCents(dollars):
    cents=int(dollars)*100
    return cents

# Routes to create listing page
@edit_item.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_listing(id):  
    currentItem=Item.query.get(id)
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        description = description.strip() # Trim white space at each end
        # item_location_id = Column(Integer)#, ForeignKey("locations.id"), index=True) #Not sure if this is needed
        price = float(request.form.get('price'))
        quantity = request.form.get('quantity')
        value = float(request.form.get('value'))
        f = request.files['photo']
        image_name = f.filename
    
        
        #item = Item.query.filter_by(name=name).first() #idk if needed to filter something first

        if request.method == 'POST' and 'photo' in request.files:
            # Need to add some type of error checking for if name exists
            # This might be a problem with displaying if file names are the same.
            # Right now it added file to folder under name_1 and still references orginal
            if f:
                photos.save(f)
                flash("Photo saved successfully.")
            # make secure_filename
            #https://stackoverflow.com/questions/53098335/flask-get-the-name-of-an-uploaded-file-minus-the-file-extension

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
        
            currentItem.name = name
            currentItem.description = description
            currentItem.quantity = quantity
            currentItem.category_id = int(category)
            currentItem.price_in_cents = price_in_cents
            currentItem.value_in_cents = value_in_cents
            if f:
                currentItem.image_name = image_name
            db.session.commit()
            flash('Item updated!', category='success')
            return redirect(url_for('views.home'))

    return render_template("edit_listing.html", user=current_user, currentItem=currentItem)