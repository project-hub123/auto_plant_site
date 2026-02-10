# app.py
# Корпоративный сайт "Автомобильный завод"

import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash

from extensions import db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "auto_plant_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(BASE_DIR, "database", "db.sqlite3")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ----------------- импорт моделей -----------------

from models.user import User
from models.article import Article
from models.news import News
from models.message import Message

# ----------------- сервисы -----------------

from services.search import search_content
from services.access_control import (
    get_current_user,
    login_required
)

# ----------------- blueprints -----------------

from blueprints.auth import auth_bp
from blueprints.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# ----------------- контекст -----------------

@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())

# ----------------- БД -----------------

@app.before_first_request
def init_db():
    os.makedirs("database", exist_ok=True)
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

# ----------------- маршруты -----------------

@app.route("/")
def index():
    news = News.query.order_by(News.id.desc()).limit(5).all()
    return render_template("index.html", news=news)


@app.route("/about")
def about():
    articles = Article.query.filter_by(category="about").all()
    return render_template("about.html", articles=articles)


@app.route("/production")
def production():
    articles = Article.query.filter_by(category="production").all()
    return render_template("production.html", articles=articles)


@app.route("/news")
def news():
    return render_template(
        "news.html",
        news=News.query.order_by(News.id.desc()).all()
    )


@app.route("/article/<int:article_id>")
def article(article_id):
    return render_template(
        "article.html",
        article=Article.query.get_or_404(article_id)
    )


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        message = Message(
            sender=request.form["name"],
            email=request.form["email"],
            text=request.form["message"]
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("contacts"))

    return render_template("contacts.html")


@app.route("/search")
def search():
    query = request.args.get("q", "")
    results = search_content(query)

    return render_template(
        "search.html",
        query=query,
        articles=results["articles"],
        news=results["news"]
    )


@app.route("/profile")
def profile():
    login_required()
    return render_template(
        "profile.html",
        user=get_current_user()
    )


@app.route("/sitemap")
def sitemap():
    return render_template("sitemap.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
