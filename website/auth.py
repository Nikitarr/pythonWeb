import email
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import views
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user 

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        contrasena = request.form.get("contrasena")

        user = User.query.filter_by(email=email).first()
        if user: 
            if check_password_hash(user.contra, contrasena):
                flash("Loggeado correctamente!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Contraseña incorrecta, proba de nuevo", category="error")
        else:
            flash("No se encontraron usuarios con ese email", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        nombre = request.form.get("nombre")
        contrasena1 = request.form.get("contrasena1")
        contrasena2 = request.form.get("contrasena2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Ya existe una cuenta asociada a ese mail", category="error")
        elif len(email) < 4:
            flash("El mail debe ser mayor que 4", category = "error")
        elif len(nombre) < 2:
            flash("El nombre debe ser mayor que 2", category = "error")
        elif contrasena1 != contrasena2:
            flash("Las contras deben coincidir", category = "error")
        elif len(contrasena1) < 5:
            flash("La constra debe ser mayor que 5", category = "error")
        else:
            new_user = User(email=email, nombre=nombre, contra=generate_password_hash(contrasena1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Cuenta creada correctamente!", category="success")
            return redirect(url_for("views.home"))



    return render_template("sign_up.html", user=current_user)


