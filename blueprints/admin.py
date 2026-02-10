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
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/", methods=["GET", "POST"])
@admin_required
def admin_panel():

    if request.method == "POST" and "article_title" in request.form:
        article = Article(
            title=request.form["article_title"],
            content=request.form["article_content"],
            category=request.form["category"]
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("admin.admin_panel"))

    if request.method == "POST" and "news_title" in request.form:
        news = News(
            title=request.form["news_title"],
            content=request.form["news_content"]
        )
        db.session.add(news)
        db.session.commit()
        return redirect(url_for("admin.admin_panel"))

    return render_template(
        "admin.html",
        users=User.query.all()
    )


@admin_bp.route("/create_user", methods=["POST"])
@admin_required
def create_user():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    if User.query.filter_by(username=username).first():
        return redirect(url_for("admin.admin_panel"))

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("admin.admin_panel"))


@admin_bp.route("/delete_user/<int:user_id>")
@admin_required
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    if user.username != "admin":
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("admin.admin_panel"))
