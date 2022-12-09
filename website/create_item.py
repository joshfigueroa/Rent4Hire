from pathlib import Path
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES
from . import db
from .models import Item

UPLOAD_FOLDER = 'website\\static\\images'
UPLOAD_PATH = Path(UPLOAD_FOLDER).resolve()

photos = UploadSet("photos", IMAGES)

create_item = Blueprint('create_item', __name__)


# Convert dollars to cents to store nicely in database
def convert_to_cents(dollars):
    cents = int(dollars) * 100
    return cents


# Routes to create listing page
@create_item.route('/create', methods=['GET', 'POST'])
@login_required
def create_listing():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        description = description.strip()  # Trim white space at each end
        # item_location_id = Column(Integer)#, ForeignKey("locations.id"), index=True) #Not sure if this is needed
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        value = request.form.get('value')
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

            new_item = Item(name=name, category_id=category,
                            description=description, owner_id=current_user.id,
                            price_in_cents=price_in_cents, quantity=quantity,
                            value_in_cents=value_in_cents, image_name=image_name)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_listing.html", user=current_user)
