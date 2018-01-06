from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(
    regex=r'',
    view=views.SearchFormView.as_view(),
    name='index'
    )
]
