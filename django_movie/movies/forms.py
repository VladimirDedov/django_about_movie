from django import forms

from .models import Reviews, Rating, RatingStar


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Reviews
        fields = ('text', 'name', 'email')


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(#Переопределение поля star, чтобы выводить звезды
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)#Widget - как представлена форма в html
    print(RatingStar.objects.all())

    class Meta:
        model = Rating
        fields = ('star',)
