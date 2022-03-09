from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import  login_required, current_user 
from .models import Note
from . import db 
import json

views = Blueprint("views", __name__)

@views.route("/", methods = ["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        nota = request.form.get("nota")

        if len(nota) < 1 :
            flash("La nota es muy corta!", category="error")
        else:
            new_nota = Note(info=nota, user_id=current_user.id)
            db.session.add(new_nota)
            db.session.commit()
            flash("Nota guardad correctamente!", category="success")    

    return render_template("home.html", user=current_user)

@views.route("/borrar-nota", methods=["POST"])

def borrar_nota():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note: 
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})  