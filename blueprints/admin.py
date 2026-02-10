# admin.py
# Административный модуль
# Проект: "Автомобильный завод"

from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    abort
)

from extensions import db
from models.user import User
from models.article import Article
from models.news import News
from services.access_control import admin_required


admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")


@admin_bp.route("/", methods=["GET", "POST"])
def admin_panel():
    admin_required()

    if request.method == "POST":
        if "article_title" in request.form:
            article = Article(
                title=request.form["article_title"],
                content=request.form["article_content"],
                category=request.form["category"]
            )
            db.session.add(article)

        if "news_title" in request.form:
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
