from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from .forms import ReviewForm


class GenreYear:
    """Жанры и года фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        list_year = Movie.objects.filter(draft=False).values("year").distinct()
        return list_year  # Выбираем из модели Movie только поле с годом


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'

    # def get(self, request):#request вся информация присланная от браузера
    #     movies = Movie.objects.all()
    #     return render(request, 'movies/movies.html', context={'movie_list': movies})


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'  # По какому полю искать запись
    template_name = 'movies/moviesingle.html'
    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     return render(request, 'movies/moviesingle.html',{'movie':movie})


class AddReview(GenreYear, View):
    """Отправка отзывов"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)  # Заполнение формы джанго
        movie = Movie.objects.get(id=pk)
        if form.is_valid():  # Проверка данных на валидность
            print('Validator true')
            form = form.save(commit=False)  # commit false - приостановка сохранения формы
            if request.POST.get("parent", None):  # Проверка на подзапрос, если есть ключ Parent имя поля из html формы
                print('Parent true')
                form.parent_id = int(request.POST.get("parent"))
                print(form.parent_id)
            # form.movie_id = pk#Привязка коммента к фильму по id
            form.movie = movie  # Привязка комента к фильму через экземляр БД Movie. Django автоматом сам привязывает
            form.save()  # Созранить форму
            print('coxp')
        return redirect(movie.get_absolute_url())  # Перенаправление на тот же адрес страницы, откуда коммент


class ActorView(GenreYear, DetailView):
    """Вывод актеров и режессеров"""
    model = Actor
    template_name = "movies/actor.html"
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Класс вывода отфильтрованных фильмов"""
    template_name = 'movies/movies.html'

    def get_queryset(self):
        if 'year' in self.request.GET and 'genre' in self.request.GET:
            queryset = Movie.objects.filter(  # Класс Q
                year__in=self.request.GET.getlist("year"),  # если года входят в список из queryseta GET запроса
                genre__in=self.request.GET.getlist("genre")  # и входят в список выбранных жанров.
            ).distinct()
        elif 'year' in self.request.GET:  # Фильтр только по годам
            queryset = Movie.objects.filter(year__in=self.request.GET.getlist("year"))
        elif 'genre' in self.request.GET:  # фильтр только по жанрам
            queryset = Movie.objects.filter(genre__in=self.request.GET.getlist("genre"))

        return queryset
