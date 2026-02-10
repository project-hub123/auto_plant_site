# message.py
# Модель сообщения обратной связи
# Проект: "Автомобильный завод"

from app import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        nullable=False
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"<Message from {self.sender}>"
