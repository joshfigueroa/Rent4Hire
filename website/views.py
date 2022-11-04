from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

# Routes to the home page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home(): # this is sample code, the home method needs to be updated to get rental listings (from area if possible)
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

# This would ne good to update to delete rental listing or something like that/ maybe even useful for deleting user
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# Routes to create listing page
@views.route('/create', methods=['GET', 'POST'])
@login_required
def create_listing():#CHANGE NAME
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("create_listing.html", user=current_user)

# Routes to create rental page
@views.route('/create_rental', methods=['GET', 'POST'])
@login_required
def create_rental():
    if request.method == 'POST':
        if request.form.get('submit_button') == "Submit":
            pass
        if request.form.get('chat_button') == "Chat":
            return render_template('chat.html', user=current_user)
    return render_template("create_rental.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    checkAuth = False
    user = current_user
    if request.method == 'POST':
        if checkAuth:
            print("here")
            if request.form['submit'] == 'submitNewInfo':
                userDB = User.query.filter_by(email = user.email).first()
                userDB.first_name = request.form.get('firstName')
                userDB.last_name = request.form.get('lastName')
                userDB.email = request.form.get('email')
                userDB.street = request.form.get('street')
                db.session.commit()
                flash("Profile Updated!", category='success')
            elif request.form['submit'] == 'Submit New Password':
                userDB = User.query.filter_by(email = user.email).first()
                new_password = request.form.get('password')
                conf_password = request.form.get('confPassword')
                if new_password == conf_password:
                    userDB.password = generate_password_hash(new_password, method='sha256')
                    db.session.commit()
                    flash("Password Updated!", category='success')
                else:
                    flash("Passwords don't match.", category='error')
        print("Here 2")
        checkPassword = request.form.get('password')
        if check_password_hash(user.password, checkPassword):
            checkAuth = True
        else:
            checkAuth = False
            flash("Incorrect credentials, try again.", category='error')
        return render_template("profile_dash.html", user = user, checkAuth = checkAuth)
    elif request.method == 'GET':
        return render_template("profile_dash.html", user = user, checkAuth = checkAuth)


# Route to a testing page, test whatever html/css you want to play with
@views.route('/test')
@login_required
def test_every():
    return render_template("test.html", user=current_user)