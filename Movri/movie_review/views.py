from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from movie_review.forms import SearchForm
from movie_review.amazon_api_utils import AmazonAPIRequest, MovieDoesNotExistException

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = 'neshto si'
        return context


class SearchFormView(FormView):
    template_name = 'search_form.html'
    form_class = SearchForm
    success_url = 'search_form.html'

    def form_valid(self, form):
        r = 'Roza'
        name = self.request.POST['movie_name']
        try:
            amazon_api = AmazonAPIRequest()
            movie = amazon_api.send_request(movie_name=name)
        except MovieDoesNotExistException:
            print('fgdfgdfgdfgdfgdffdgdfgdfgfdgdfgdf')
        import ipdb; ipdb.set_trace()
        return super().form_valid(form)
