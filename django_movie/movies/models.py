from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['id', ]  # сортировка в админ панеле

class Actor(models.Model):
    """Актерыи режиссеры"""
    name = models.CharField(max_length=100, verbose_name='ФИО')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(verbose_name='Описание')
    img = models.ImageField(upload_to="actors/", verbose_name="Изображение")

    def get_absolut_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField(max_length=100, verbose_name='Название Жанра')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Фильмы"""
    title = models.CharField(max_length=100, verbose_name='Название фильма')
    tagline = models.CharField(max_length=100, verbose_name='Слоган фильма', default='')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(upload_to='movies/', verbose_name='Постер')
    year = models.PositiveSmallIntegerField(default=2022, verbose_name='Дата выхода')
    country = models.CharField(max_length=100, verbose_name='Страна')
    directors = models.ManyToManyField(Actor, related_name='film_derector', verbose_name='Режиссеры')
    actors = models.ManyToManyField(Actor, related_name='film_actor', verbose_name='Актеры')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    world_premiere = models.DateField(default=date.today, verbose_name='Премьера в мире')
    budget = models.PositiveIntegerField(default=0, verbose_name='Бюджет', help_text="Сумма в долларах")
    fees_in_usa = models.PositiveIntegerField(default=0, verbose_name='Сборы в сша')
    fees_in_world = models.PositiveIntegerField(default=0, verbose_name='Сборы в мире')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    url = models.SlugField(max_length=130, unique=True, db_index=True, verbose_name='URL')
    draft = models.BooleanField(default=False, verbose_name='Черновик')

    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews_set.filter(
            parent__isnull=True)  # Возвращает список отзывов прикрепленных к фильму, где поле parent равно Null. Только родительские отзывы

    def get_absolute_url(self):  # Метод формирования URL адреса по слагу
        return reverse('movie_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering=['id',]#сортировка в админ панеле


class Movie_Shots(models.Model):
    """Кадры из фильма"""
    title = models.CharField(max_length=100, verbose_name='Название фильма')
    description = models.TextField(verbose_name='Описание')
    img = models.ImageField(upload_to="movie_shorts/", verbose_name='Изображение')  # Пока пропустить
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.SmallIntegerField(default=0, verbose_name='Значение')

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering=['-value']


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField(max_length=15, verbose_name='IP адрес')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы к фильмам"""
    email = models.EmailField(max_length=50, verbose_name='E-mail')
    name = models.CharField(max_length=255, verbose_name='Имя')
    text = models.TextField(verbose_name='Описание')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name="Родитель")  # пока не понятно
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
