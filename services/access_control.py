# services/access_control.py
# Сервис контроля доступа и ролей пользователей
# Проект: "Автомобильный завод"

from functools import wraps
from flask import session, abort, redirect, url_for
from models.user import User


def get_current_user():
    """
    Возвращает текущего авторизованного пользователя
    или None, если пользователь не вошёл в систему.
    """
    user_id = session.get("user_id")
    if not user_id:
        return None

    return User.query.get(user_id)


def login_required(func):
    """
    Декоратор проверки авторизации пользователя.
    Если пользователь не вошёл в систему — редирект на страницу входа.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """
    Декоратор проверки прав администратора.
    Если пользователь не администратор — ошибка 403.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_admin():
            abort(403)
        return func(*args, **kwargs)
    return wrapper
