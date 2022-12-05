from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user

from flask_wtf import FlaskForm

from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired
from wtforms import SubmitField

from . import db
from .models import Item, Category, Order
import datetime

order_item = Blueprint('order_item', __name__)

# Displays the date/time UI functions
class OrderFormInfo(FlaskForm):
    scheduled_pickup_date = DateTimeLocalField('Schedule Pickup', format='%Y-%m-%dT%H:%M', validators=(DataRequired('** Required'),InputRequired(),))
    scheduled_return_date = DateTimeLocalField('Schedule Return', format='%Y-%m-%dT%H:%M', validators=(DataRequired('** Required'),InputRequired(),))
    submit = SubmitField('Schedule') #OR RESERVE???


# page for individual items. gets passed the item id, returns the object.
@order_item.route('order/item/<id>', methods=['GET', 'POST'] )
@login_required
def display_item(id):
    # Creates date/time form
    form = OrderFormInfo()
    currentItem=Item.query.get(id)
    category=Category.query.get(currentItem.category_id)
    if request.method == 'POST':
        # Does error checking for scheduled pickup/return
        if form.scheduled_pickup_date.data < datetime.datetime.now(): 
            flash("Pickup date can't be in the past.", category='error')
        elif form.scheduled_pickup_date.data > (datetime.datetime.now() + datetime.timedelta(days=3)):  
            flash("Can only reserve items within 3 days.", category='error')
        elif form.scheduled_return_date.data < form.scheduled_pickup_date.data: 
            flash("Return date can't be in the past or before pickup date.", category='error')
        else:
            quantity = request.form.get('quantity')
            # Grabs picked dates/times
            session['scheduled_pickup_date'] = form.scheduled_pickup_date.data
            session['scheduled_return_date'] = form.scheduled_return_date.data
            # Create order in database
            create_order(session['scheduled_pickup_date'], session['scheduled_return_date'], id, quantity)
            flash('Order Scheduled! Visit profile to confirm pickup.', category='success')
            return redirect(url_for('views.home'))
    return render_template('order.html', user=current_user, currentItem=currentItem,
                           category=category, form=form)
 
 
 # WILL DELETE SOON
# !!!!!Added right now to see how it works  /redirects from item/id/!!!!!!!! 
#!!!! is a static ---see if its useful!!!!!
@order_item.route('static/date/<id>', methods=['GET','POST'])
@login_required
def date(id):
    
    scheduled_pickup_date = session['scheduled_pickup_date']
    scheduled_return_date = session['scheduled_return_date']
    return render_template('date.html', user=current_user, currentItem=Item.query.get(id))


def create_order(scheduled_pickup_date, scheduled_return_date, item_id, quantity):
    new_order = Order(renter_id=current_user.id, scheduled_pickup_date=scheduled_pickup_date, 
                        scheduled_return_date=scheduled_return_date, item_id=item_id,
                        is_active=True, quantity=quantity,) # When is_active = True, item stays out of search- update item avail
    item = Item.query.filter_by(id=item_id).first()
    item.is_available = False
    db.session.add(new_order)
    db.session.commit()