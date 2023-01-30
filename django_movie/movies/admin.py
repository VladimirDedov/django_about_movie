from django.contrib import admin

from django import forms
from .models import *
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

#Настройка для редактора CKEditor
class MovieAdminForm(forms.ModelForm):#Подключить форму к классу MovieAdmin
    description = forms.CharField(label='Описание фильма', widget=CKEditorUploadingWidget())#Поле отвечающее за описание фильма добавляем виджет
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(
    Category)  # Регистрация класса с помощью декоратора аналогично - admin.site.register(Category, CategoryAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name', 'url')
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'url': ('name',)}
    list_ = ('id',)


class ReviewInLine(admin.TabularInline):  # Класс для отображения привязанных отзывов в редактировании фильма
    model = Reviews
    extra = 1  # Количество дополнительных полей при добавлении коментов в фильме
    readonly_fields = ('name', 'email')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'title', 'category', 'poster', 'year', 'country', 'world_premiere', 'budget', 'url', 'draft')
    list_display_links = ('title', 'year', 'country', 'world_premiere', 'category', 'url')
    list_editable = ('draft',)
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')  # __ Обращение к связанной модели
    # inlines = [ReviewInLine]  # Передается класс
    save_on_top = True  # Перенос меню сохранения(кнопок) на верх
    save_as = True  # Появляется кнопка "Сохранить как новый объект" при изменении нескольких полей
    readonly_fields = ('get_image',)#Добавление картинки постера
    form=MovieAdminForm#Подключение формы описанной выше для CKEditor
    fieldsets = (  # Группировка по полям
        (None, {'fields': (('title', 'tagline'),)}),  # В одну строчку выводятся данные
        ('Постер', {'fields': (('poster', 'get_image'),)}),
        ('Даты', {'fields': (('year', 'world_premiere', 'country'),)}),
        ('Люди', {
            'classes': ('collapse',),  # Скрывает поля в админке при редактировании
            'fields': (('actors', 'directors'),)}),
        ('Жанр', {
            'classes': ('collapse',),
            'fields': (('genre', 'category'),)}),
        ('Описание фильма', {'fields': ('description',)})
    )


    def get_image(self, obj):  # obj - объект класса Actor
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie')
    readonly_fields = ('name', 'email')  # Скрытые от редактирования поля


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)  # вывод изображения в самой записи

    # Метод дл вывода изображения в админке
    def get_image(self, obj):  # obj - объект класса Actor
        return mark_safe(f'<img src={obj.img.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Movie_Shots)
class Movie_ShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):  # obj - объект класса Actor
        return mark_safe(f'<img src={obj.img.url} width="80" height="60"')

    get_image.short_description = 'Изображение'


# admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
# admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(RatingStar)

admin.site.site_title = "Django-movies"# Изменение названия самой админ панели
admin.site.site_header = "Django-movies"# Изменение названия самой админ панели