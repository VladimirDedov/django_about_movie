from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import *
from .forms import ReviewForm, RatingForm


class GenreYear:
    """Жанры и года фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        new_lst_year_distinct = []
        list_year = Movie.objects.filter(draft=False).values("year").distinct()
        for dct in list_year:
            if dct not in new_lst_year_distinct:
                new_lst_year_distinct.append(dct)
        return new_lst_year_distinct  # Выбираем из модели Movie только поле с годом


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'

    # def get(self, request):#request вся информация присланная от браузера
    #     movies = Movie.objects.all()
    #     return render(request, 'movies/movies.html', context={'movie_list': movies})


class Search(GenreYear, ListView):
    """Поиск фильмов"""
    template_name = 'movies/movies.html'

    def get_queryset(self): # q - имя поля input из sidebar.html
        paginate_by = 3
        queryset = Movie.objects.filter(title__iregex=self.request.GET.get("q"))  # __icontains - искать без учета регистра
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        print(context['q'])
        return context


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'  # По какому полю искать запись
    template_name = 'movies/moviesingle.html'

    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     return render(request, 'movies/moviesingle.html',{'movie':movie})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


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


class AddStarRating(View):
    """Добавление рейтинга фильма"""

    def get_clients_ip(self, request):
        """получение ip клиента"""
        x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward_for:
            ip = x_forward_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        """Установка рейтинга фильма"""
        form = RatingForm(request.POST)  # Генерация формы на основе request
        if form.is_valid():
            Rating.objects.update_or_create(  # Создать или обновить поля в модели
                ip=self.get_clients_ip(request),  # Получить ip клиента
                movie_id=int(request.POST.get('movie')),
                # Передается поле movie from POST запроса. Приходят из скрытого поля input movie
                defaults={"star_id": int(request.POST.get("star"))}
                # Словарь, поле которое хотим изменить, если запись найдена и создать если нет.
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
