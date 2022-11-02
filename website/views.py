from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
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

# Route to a testing page, test whatever html/css you want to play with
@views.route('/test')
@login_required
def test_every():
    return render_template("test.html", user=current_user)