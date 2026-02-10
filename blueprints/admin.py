# admin.py
# Административный модуль (Blueprint)
# Проект: "Автомобильный завод"

from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    session, abort
)

from app import db
from app import User, Article, News


admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")


# -------------------------------------------------
# ВСПОМОГАТЕЛЬНАЯ ПРОВЕРКА ДОСТУПА
# -------------------------------------------------

def is_admin():
    user_id = session.get("user_id")
    if not user_id:
        return False

    user = User.query.get(user_id)
    if not user:
        return False

    return user.role == "admin"


# -------------------------------------------------
# ГЛАВНАЯ СТРАНИЦА АДМИН-ПАНЕЛИ
# -------------------------------------------------

@admin_bp.route("/", methods=["GET", "POST"])
def admin_panel():
    if not is_admin():
        abort(403)

    # -----------------------------
    # ДОБАВЛЕНИЕ СТАТЬИ
    # -----------------------------
    if request.method == "POST" and "article_title" in request.form:
        article = Article(
            title=request.form.get("article_title"),
            content=request.form.get("article_content"),
            category=request.form.get("category")
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("admin_bp.admin_panel"))

    # -----------------------------
    # ДОБАВЛЕНИЕ НОВОСТИ
    # -----------------------------
    if request.method == "POST" and "news_title" in request.form:
        news = News(
            title=request.form.get("news_title"),
            content=request.form.get("news_content")
        )
        db.session.add(news)
        db.session.commit()
        return redirect(url_for("admin_bp.admin_panel"))

    articles = Article.query.all()
    news = News.query.all()
    users = User.query.all()

    return render_template(
        "admin.html",
        articles=articles,
        news=news,
        users=users
    )


# -------------------------------------------------
# УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ
# -------------------------------------------------

@admin_bp.route("/user/<int:user_id>/set_role/<role>")
def set_user_role(user_id, role):
    if not is_admin():
        abort(403)

    user = User.query.get_or_404(user_id)

    if role in ["admin", "user"]:
        user.role = role
        db.session.commit()

    return redirect(url_for("admin_bp.admin_panel"))
