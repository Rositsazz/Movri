from django import forms


class SearchForm(forms.Form):
    movie_name = forms.CharField(label='Movie name', max_length=150)
