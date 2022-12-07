from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import uuid


# Method to generate a unique id for any object.
# Casts to an int for compatability with sqlalchemy.

def generate_uuid():
    return int(uuid.uuid4())


# This will be deleted, this is an example for rental listings
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=generate_uuid())
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):  # LEFT OUT TABLE NAMES BC IT COMPLICATED THINGS
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)

    date_created = db.Column(db.DATETIME, default=datetime.utcnow, index=True)

    street = db.Column(db.String(255))  # LEAVING NULLABLE SO NOT SO DEMANDING AT SIGN UP
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    # ADD A PHONE NUMBER!!!!!!

    items = db.relationship("Item", backref="owner")
    orders = db.relationship("Order", backref="renter")
    reviews = db.relationship("Review", backref="user")


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), index=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    description = db.Column(db.Text, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # ??????????
    date_created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    # item_location_id = Column(Integer)#, ForeignKey("locations.id"), index=True) #Not sure if this is needed
    price_in_cents = db.Column(db.Integer, nullable=False, index=True)  # Same thing here
    quantity = db.Column(db.Integer, default=1, index=True) 
    value_in_cents = db.Column(db.Integer, nullable=False, index=True) 
    image_name = db.Column(db.String(255), index=True)

    item_reviews = db.relationship("Review", backref="item")  # the item being reviewed
    orders = db.relationship("Order", backref="item")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    renter_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    scheduled_pickup_date = db.Column(db.DateTime, nullable=False)    # Take strftime out of views form .data 
    scheduled_return_date = db.Column(db.DateTime, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), index=True)
    actual_pickup_date = db.Column(db.DateTime)    # Take strftime out of views form .data 
    actual_return_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Integer)
    

# add location in profile
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(5), nullable=False)
    # country = db.Column(db.String(255), nullable=False) # Deleted this

    users = db.relationship("User", backref="location")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    category = db.Column(db.String(255), index=True)

    items = db.relationship("Item", backref="category")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    reviewer = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    reviewed_item = db.Column(db.Integer, db.ForeignKey("item.id"), index=True)
    date_created = db.Column(db.DATETIME, default=datetime.utcnow, index=True)
    title = db.Column(db.String(255), index=True)
    description = db.Column(db.Text, index=True)
