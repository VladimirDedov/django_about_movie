from django.views.generic import  ListView, DetailView, View
from django.shortcuts import render, redirect
from .models import *
from .forms import ReviewForm



class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'



    # def get(self, request):#request вся информация присланная от браузера
    #     movies = Movie.objects.all()
    #     return render(request, 'movies/movies.html', context={'movie_list': movies})

class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'#По какому полю искать запись
    template_name = 'movies/moviesingle.html'
    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     return render(request, 'movies/moviesingle.html',{'movie':movie})

class AddReview(View):
    """Отправка отзывов"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)#Заполнение формы джанго
        movie = Movie.objects.get(id=pk)
        if form.is_valid():#Проверка данных на валидность
            print('Validator true')
            form = form.save(commit=False)  # commit false - приостановка сохранения формы
            if request.POST.get("parent", None):#Проверка на подзапрос, если есть ключ Parent имя поля из html формы
                print('Parent true')
                form.parent_id = int(request.POST.get("parent"))
                print(form.parent_id)
            #form.movie_id = pk#Привязка коммента к фильму по id
            form.movie = movie# Привязка комента к фильму через экземляр БД Movie. Django автоматом сам привязывает
            form.save()#Созранить форму
            print('coxp')
        return redirect(movie.get_absolute_url())#Перенаправление на тот же адрес страницы, откуда коммент