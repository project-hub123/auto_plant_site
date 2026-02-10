# access_control.py
# Сервис контроля доступа и ролей пользователей
# Проект: "Автомобильный завод"

from flask import session, abort
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


def login_required():
    """
    Проверка авторизации пользователя.
    Если пользователь не вошёл в систему — ошибка 403.
    """
    if not session.get("user_id"):
        abort(403)


def admin_required():
    """
    Проверка прав администратора.
    Если пользователь не администратор — ошибка 403.
    """
    user = get_current_user()
    if not user or not user.is_admin():
        abort(403)
