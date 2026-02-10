# news.py
# Модель новости
# Проект: "Автомобильный завод"

from extensions import db


class News(db.Model):
    __tablename__ = "news"

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

    def __repr__(self):
        return f"<News {self.title}>"
