from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import uuid

# Method to generate a unique id for any object.
# Casts to an int for compatability with sqlalchemy.

def generate_uuid():
    return int(uuid.uuid4())

# This will be delete, this is an example for rental listings
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=generate_uuid())
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):#LEFT OUT TABLE NAMES BC IT COMPLICATED THINGS
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    notes = db.relationship('Note') #Will be deleted
    
    date_created = db.Column(db.DATETIME, default=datetime.utcnow, index=True)
    
    street = db.Column(db.String(255))# LEAVING NULLABLE SO NOT SO DEMANDING AT SIGN UP
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    #availability = db.Column(db.DATETIME) #???????? if a owner -> avail = not nullable UPDATE TOOK OUT TO SIMPLIFY
    #ADD A PHONE NUMBER!!!!!!
    
    items = db.relationship("Item", backref="owner")
    orders = db.relationship("Order", backref="renter")
    reviews = db.relationship("Review", backref="user")

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), index=True)
    availability = db.Column(db.DATETIME) #, nullable=False???????????
    description = db.Column(db.Text, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))#??????????
    date_created = db.Column(db.DATETIME, default=datetime.utcnow, index=True)
    #item_location_id = Column(Integer)#, ForeignKey("locations.id"), index=True) #Not sure if this is needed
    price_in_cents = db.Column(db.Integer, nullable=False, index=True) #Same thing here
    
    item_reviews = db.relationship("Review", backref="item") #its the item being reviewed
    orders = db.relationship("Order", backref="item")
 
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    date_created = db.Column(db.DATETIME, default=datetime.utcnow, index=True)
    renter_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    pickup_date = db.Column(db.DATETIME, nullable=False)
    dropoff_date = db.Column(db.DATETIME, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), index=True) 
    #add total
    
    #transaction = relationship("Transaction", backref="order", uselist=False) #one-to-one rel IF USING TRANSACTION TABLE
    
#add location etc in profile
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(5), nullable=False)
    #country = db.Column(db.String(255), nullable=False) # Deleted this 
    
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
    descritpion = db.Column(db.Text, index=True)
