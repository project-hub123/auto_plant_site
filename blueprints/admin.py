# admin.py
# Административный модуль
# Проект: "Автомобильный завод"

from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    abort
)

from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User
from models.article import Article
from models.news import News
from services.access_control import admin_required


admin_bp = Blueprint(
    "admin_bp",
    __name__,
    url_prefix="/admin"
)


# -------------------------------------------------
# ГЛАВНАЯ СТРАНИЦА АДМИН-ПАНЕЛИ
# -------------------------------------------------

@admin_bp.route("/", methods=["GET", "POST"])
def admin_panel():
    admin_required()

    # добавление статьи
    if request.method == "POST" and "article_title" in request.form:
        article = Article(
            title=request.form["article_title"],
            content=request.form["article_content"],
            category=request.form["category"]
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("admin_bp.admin_panel"))

    # добавление новости
    if request.method == "POST" and "news_title" in request.form:
        news = News(
            title=request.form["news_title"],
            content=request.form["news_content"]
        )
        db.session.add(news)
        db.session.commit()
        return redirect(url_for("admin_bp.admin_panel"))

    return render_template(
        "admin.html",
        articles=Article.query.all(),
        news=News.query.all(),
        users=User.query.all()
    )


# -------------------------------------------------
# СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ
# -------------------------------------------------

@admin_bp.route("/create_user", methods=["POST"])
def create_user():
    admin_required()

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    if User.query.filter_by(username=username).first():
        return redirect(url_for("admin_bp.admin_panel"))

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("admin_bp.admin_panel"))


# -------------------------------------------------
# УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
# -------------------------------------------------

@admin_bp.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)

    # запрещаем удалять главного администратора
    if user.username != "admin":
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("admin_bp.admin_panel"))
