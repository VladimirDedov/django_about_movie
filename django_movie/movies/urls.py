from django.urls import path
from .views import *
urlpatterns =[
    path('', MoviesView.as_view(), name='MovieList'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),#Имя используются в html форме в теге {% url "Name_path" %}
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path("search/",Search.as_view(), name="search"),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", ActorView.as_view(), name="actor_detail")

]