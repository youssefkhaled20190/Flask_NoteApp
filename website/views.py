
from . import db
import json
from .models import Notes
from flask import Blueprint, jsonify, render_template, flash, request
from flask_login import login_required, current_user
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# this decoretor will run when user login only but not vice versa
@login_required
def Home():

    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short !', category='error')
        else:
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added successfuly', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # this function expects a JSON from the INDEX.js file
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
