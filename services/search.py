# search.py
# Сервис поиска по сайту
# Проект: "Автомобильный завод"

from models.article import Article
from models.news import News


def search_content(query: str):
    """
    Выполняет поиск по статьям и новостям сайта.

    :param query: поисковый запрос
    :return: словарь с результатами поиска
    """

    if not query or len(query.strip()) < 2:
        return {
            "articles": [],
            "news": []
        }

    query = query.strip()

    # Поиск по заголовкам и тексту статей
    articles = Article.query.filter(
        (Article.title.ilike(f"%{query}%")) |
        (Article.content.ilike(f"%{query}%"))
    ).all()

    # Поиск по заголовкам и тексту новостей
    news = News.query.filter(
        (News.title.ilike(f"%{query}%")) |
        (News.content.ilike(f"%{query}%"))
    ).all()

    return {
        "articles": articles,
        "news": news
    }
