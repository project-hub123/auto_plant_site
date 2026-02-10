# auth.py
# Модуль авторизации и регистрации пользователей
# Проект: "Автомобильный завод"

from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    session
)
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import User


auth_bp = Blueprint("auth", __name__)


# -------------------------------------------------
# ВХОД В СИСТЕМУ
# -------------------------------------------------

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


# -------------------------------------------------
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# -------------------------------------------------

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            error = "Пользователь с таким логином уже существует"
        else:
            new_user = User(
                username=username,
                password_hash=generate_password_hash(password),
                role="user"
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template("register.html", error=error)


# -------------------------------------------------
# ВЫХОД ИЗ СИСТЕМЫ
# -------------------------------------------------

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
