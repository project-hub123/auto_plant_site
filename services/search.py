# search.py
# Сервис поиска по сайту
# Проект: "Автомобильный завод"

from sqlalchemy import or_
from models.article import Article
from models.news import News


def search_content(query: str):
    """
    Выполняет поиск по статьям и новостям сайта.
    Возвращает словарь с результатами.
    """

    if not query:
        return {"articles": [], "news": []}

    query = query.strip()

    if len(query) < 2:
        return {"articles": [], "news": []}

    try:
        articles = Article.query.filter(
            or_(
                Article.title.ilike(f"%{query}%"),
                Article.content.ilike(f"%{query}%")
            )
        ).all()

        news = News.query.filter(
            or_(
                News.title.ilike(f"%{query}%"),
                News.content.ilike(f"%{query}%")
            )
        ).all()

    except Exception:
        # если вдруг что-то в базе не так — не роняем сайт
        return {"articles": [], "news": []}

    return {
        "articles": articles or [],
        "news": news or []
    }
