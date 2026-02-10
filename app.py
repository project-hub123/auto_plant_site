# app.py
# Корпоративный сайт "Автомобильный завод"
# Практика: разработка веб-сайта без CMS
# Стек: Python + Flask

import os
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, abort
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------------------------
# НАСТРОЙКИ ПРИЛОЖЕНИЯ
# -------------------------------------------------

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "auto_plant_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database", "db.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------------------------
# МОДЕЛИ БАЗЫ ДАННЫХ
# -------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

# -------------------------------------------------
# ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ
# -------------------------------------------------

@app.before_first_request
def create_tables():
    db.create_all()

    # создаём администратора, если его нет
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

# -------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -------------------------------------------------

def current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None


def login_required():
    if "user_id" not in session:
        return False
    return True


def admin_required():
    user = current_user()
    return user and user.role == "admin"

# -------------------------------------------------
# ОСНОВНЫЕ СТРАНИЦЫ
# -------------------------------------------------

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
    all_news = News.query.order_by(News.id.desc()).all()
    return render_template("news.html", news=all_news)


@app.route("/article/<int:article_id>")
def article(article_id):
    art = Article.query.get_or_404(article_id)
    return render_template("article.html", article=art)


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

# -------------------------------------------------
# ПОИСК ПО САЙТУ
# -------------------------------------------------

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    articles = []
    news = []

    if query:
        articles = Article.query.filter(Article.title.contains(query)).all()
        news = News.query.filter(News.title.contains(query)).all()

    return render_template(
        "search.html",
        query=query,
        articles=articles,
        news=news
    )

# -------------------------------------------------
# АВТОРИЗАЦИЯ И РЕГИСТРАЦИЯ
# -------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.check_password(request.form["password"]):
            session["user_id"] = user.id
            return redirect(url_for("profile"))
        else:
            error = "Неверный логин или пароль"

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        if User.query.filter_by(username=request.form["username"]).first():
            error = "Пользователь уже существует"
        else:
            user = User(
                username=request.form["username"],
                password_hash=generate_password_hash(request.form["password"]),
                role="user"
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template("register.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# -------------------------------------------------
# ЛИЧНЫЙ КАБИНЕТ
# -------------------------------------------------

@app.route("/profile")
def profile():
    if not login_required():
        return redirect(url_for("login"))

    user = current_user()
    return render_template("profile.html", user=user)

# -------------------------------------------------
# АДМИН-ПАНЕЛЬ
# -------------------------------------------------

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not admin_required():
        abort(403)

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
        return redirect(url_for("admin"))

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
# КАРТА САЙТА
# -------------------------------------------------

@app.route("/sitemap")
def sitemap():
    return render_template("sitemap.html")

# -------------------------------------------------
# СТРАНИЦА 404
# -------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# -------------------------------------------------
# ЗАПУСК ПРИЛОЖЕНИЯ
# -------------------------------------------------

if __name__ == "__main__":
    os.makedirs("database", exist_ok=True)
    app.run(debug=True)
