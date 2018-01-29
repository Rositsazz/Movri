from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from movie_review.forms import SearchForm
from movie_review.models import Movie
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

    # def get_success_url(self):
    #     return reverse('movie-reviews')

    def get_success_url(self):
        return reverse_lazy('movie-reviews:movie-reviews',
                       kwargs={'movie_name': self.kwargs.get('movie_name')})

    def form_valid(self, form):
        name = self.request.POST['movie_name']
        import ipdb; ipdb.set_trace()
        self.kwargs['movie_name'] = name
        try:
            amazon_api = AmazonAPIRequest()
            movie_data = amazon_api.send_request(movie_name=name)
            movie_obj, is_created = Movie.objects.get_or_create(
                name=movie_data.title)
            movie_obj.reviews_url = movie_data.reviews[1]
            movie_obj.asin = movie_data.asin
            movie_obj.save()
        except MovieDoesNotExistException:
            print('THE MOVIE DOES NOT EXIST')
        # import ipdb; ipdb.set_trace()
        return super().form_valid(form)


class MovieReviewsView(TemplateView):
    template_name = 'movie_reviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import ipdb; ipdb.set_trace()
        context['movie_name'] = self.kwargs['movie_name']
        return context
