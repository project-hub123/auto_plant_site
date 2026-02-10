# user.py
# Модель пользователя
# Проект: "Автомобильный завод"

from extensions import db
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )

    def check_password(self, password: str) -> bool:
        """
        Проверка пароля пользователя
        """
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        """
        Проверка, является ли пользователь администратором
        """
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.username}, role={self.role}>"
