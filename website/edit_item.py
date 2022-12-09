from pathlib import Path
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES
from . import db
from .models import Item

UPLOAD_FOLDER = 'website\\static\\images'
UPLOAD_PATH = Path(UPLOAD_FOLDER).resolve()

photos = UploadSet("photos", IMAGES)

edit_item = Blueprint('edit_item', __name__)


# Convert dollars to cents to store nicely in database
def convert_to_cents(dollars):
    cents = int(dollars) * 100
    return cents


# Routes to create listing page
@edit_item.route('/edit/<listing_id>', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    current_item = Item.query.get(listing_id)
    if request.method == 'POST':

        if request.form.get('edited') == 'edited':
            print('hello')
            name = request.form.get('name')
            category = request.form.get('category')
            description = request.form.get('description')
            description = description.strip()  # Trim white space at each end
            # item_location_id = Column(Integer)#, ForeignKey("locations.id"), index=True) #Not sure if this is needed
            price = float(request.form.get('price'))
            quantity = request.form.get('quantity')
            value = float(request.form.get('value'))
            f = request.files['photo']
            image_name = f.filename

            # item = Item.query.filter_by(name=name).first() #idk if needed to filter something first

            if request.method == 'POST' and 'photo' in request.files:
                # Need to add some type of error checking for if name exists
                # This might be a problem with displaying if file names are the same.
                # Right now it added file to folder under name_1 and still references orginal
                if f:
                    photos.save(f)
                    flash("Photo saved successfully.")
                # make secure_filename
                # https://stackoverflow.com/questions/53098335/flask-get-the-name-of-an-uploaded-file-minus-the-file-extension

            # ERROR CHECKING
            if len(name) < 1:
                flash('Name is too short', category='error')
            elif len(name) > 254:
                flash('Name max character count is 255', category='error')
            elif len(description) < 1:
                flash('Insert descripton', category='error')
            elif quantity is None:
                flash('Select a quantity', category='error')
            elif price is None:
                flash('Input price', category='error')
            elif value is None:
                flash('Input value', category='error')
            else:
                # NEED TO ADD PICTURE INFO LATER!!!!!!!!!!!!

                # Convert string to integer
                # category=int(categoryStr)

                # Convert dollars to cents
                price_in_cents = convert_to_cents(price)
                value_in_cents = convert_to_cents(value)

                current_item.name = name
                current_item.description = description
                current_item.quantity = quantity
                current_item.category_id = int(category)
                current_item.price_in_cents = price_in_cents
                current_item.value_in_cents = value_in_cents
                if f:
                    current_item.image_name = image_name
                db.session.commit()
                flash('Item updated!', category='success')
                return redirect(url_for('views.home'))

        elif request.form.get('deleted') == 'Delete':
            print('hi')
            db.session.delete(current_item)
            db.session.commit()
            flash('Item Deleted!', category='success')
            return redirect(url_for('views.home'))

    return render_template("edit_listing.html", user=current_user, currentItem=current_item)
