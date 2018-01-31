from django.conf.urls import url
from . import views

app_name = 'movie-reviews'

urlpatterns = [
    url(
        regex=r'^$',
        view=views.SearchFormView.as_view(),
        name='movie-search'
    ),
    url(
        regex=r'reviews/(?P<movie_name>[-\'\:\w ]+)$',
        view=views.MovieReviewsView.as_view(),
        name='movie-reviews'
    )
]
