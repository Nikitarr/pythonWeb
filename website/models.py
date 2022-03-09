from email.policy import default
from enum import unique
from sqlalchemy import func
from website import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(10000))
    fecha = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    contra = db.Column(db.String(150))
    nombre = db.Column(db.String(150))
    notes = db.relationship("Note")