from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    session
)
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.user import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("profile"))
        else:
            error = "Неверный логин или пароль"

    return render_template("login.html", error=error)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error = "Заполните все поля"
        elif User.query.filter_by(username=username).first():
            error = "Пользователь с таким логином уже существует"
        else:
            user = User(
                username=username,
                password_hash=generate_password_hash(password),
                role="user"
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template("register.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
