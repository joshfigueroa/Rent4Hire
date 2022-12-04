from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user

from flask_wtf import FlaskForm

from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired
from wtforms import SubmitField

from .models import Item, Category
import datetime

order_item = Blueprint('order_item', __name__)

# Displays the date/time UI functions
class OrderFormInfo(FlaskForm):
    scheduled_pickup_date = DateTimeLocalField('Schedule Pickup', format='%Y-%m-%dT%H:%M', validators=(DataRequired('** Required'),InputRequired(),))
    scheduled_return_date = DateTimeLocalField('Schedule Return', format='%Y-%m-%dT%H:%M', validators=(DataRequired('** Required'),InputRequired(),))
    submit = SubmitField('Schedule') #OR RESERVE???


# page for individual items. gets passed the item id, returns the object.
@order_item.route('/item/<id>', methods=['GET', 'POST'] )
@login_required
def display_item(id):
    # Creates date/time form
    form = OrderFormInfo()
    if request.method == 'POST':
        # Does error checking for scheduled pickup/return
        if form.scheduled_pickup_date.data < datetime.datetime.now(): 
            flash("Pickup date can't be in the past.", category='error')
        elif form.scheduled_pickup_date.data > (datetime.datetime.now() + datetime.timedelta(days=3)):  
            flash("Can only reserve items within 3 days.", category='error')
        elif form.scheduled_return_date.data < form.scheduled_pickup_date.data: # (datetime.datetime.now() + datetime.timedelta(days=10)) > 
            flash("Return date can't be in the past or before pickup date.", category='error')
        else:
            # Grabs picked dates/times
            session['scheduled_pickup_date'] = form.scheduled_pickup_date.data.strftime("%Y-%m-%d %H:%M:%S %p")
            session['scheduled_return_date'] = form.scheduled_return_date.data.strftime("%Y-%m-%d %H:%M:%S %p")
            return redirect(url_for('static',filename='date/' + id), code=301)
    return render_template('item.html', user=current_user, currentItem=Item.query.get(id),
                           category=Category.query.all(), form=form)
 
# !!!!!Added right now to see how it works  /redirects from item/id/!!!!!!!! 
#!!!! is a static ---see if its useful!!!!!
@order_item.route('static/date/<id>', methods=['GET','POST'])
@login_required
def date(id):
    
    scheduled_pickup_date = session['scheduled_pickup_date']
    scheduled_return_date = session['scheduled_return_date']
    return render_template('date.html', user=current_user, currentItem=Item.query.get(id))