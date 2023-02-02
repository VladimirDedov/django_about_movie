from django import template
from movies.models import Category, Movie
register = template.Library()#Экземпляр класса Library

@register.simple_tag#Декоратор регистрирует функцию как тег
def get_categories():#Возвращает в словарь last_movie во view
    """Вывод все катерий"""
    return Category.objects.all()

@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    """Вывод последних добавленных фильмов"""
    movie = Movie.objects.order_by('id')[:count]
    return {'last_movies':movie}
