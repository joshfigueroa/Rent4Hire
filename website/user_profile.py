from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User
from . import db


user_profile = Blueprint('user_profile', __name__)

# SHOULD BE ABLE TO DELETE!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Routes to create rental profile
@user_profile.route('/rental_profile', methods=['GET', 'POST'])
@login_required
def rental_profile():
    if request.method == 'POST':
        if request.form.get('submit_button') == "Submit":
            pass
        if request.form.get('chat_button') == "Chat":
            return render_template('chat.html', user=current_user)
    return render_template("rental_profile.html", user=current_user)


@user_profile.route('/profile', methods=['GET', 'POST'])
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
