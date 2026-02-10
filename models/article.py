# article.py
# Модель статьи
# Проект: "Автомобильный завод"

from extensions import db


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    def __repr__(self):
        return f"<Article {self.title}, category={self.category}>"
