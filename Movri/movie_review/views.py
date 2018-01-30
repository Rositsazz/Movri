from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from movie_review.forms import SearchForm
from movie_review.models import Movie, Review
from movie_review.amazon_api_utils import AmazonAPIRequest, MovieDoesNotExistException
from movie_review.reviews_parser import ReviewParser


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = 'neshto si'
        return context


class SearchFormView(FormView):
    template_name = 'search_form.html'
    form_class = SearchForm

    def get_success_url(self):
        return reverse_lazy('movie-reviews:movie-reviews',
                            kwargs={'movie_name': self.kwargs.get('movie_name')})

    def form_valid(self, form):
        name = self.request.POST['movie_name']
        self.kwargs['movie_name'] = name

        movie, created = Movie.objects.get_or_create(name=name.lower())
        if created:
            try:
                amazon_api = AmazonAPIRequest()
                movie_data = amazon_api.send_request(movie_name=name)
                movie.asin = movie_data.asin
                movie.name = movie_data.title.lower()
                movie.reviews_url = movie_data.reviews[1]
                movie.save()
                parser = ReviewParser(asin=movie.asin, name=movie.name)
                most_recent_reviews = parser.most_recent_reviews(
                    number_of_reviews=100)
                parser.create_review_objects(most_recent_reviews)
            except MovieDoesNotExistException:
                print('THE MOVIE DOES NOT EXIST')
        return super().form_valid(form)


class MovieReviewsView(TemplateView):
    template_name = 'movie_reviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = self.kwargs['movie_name']
        movie = Movie.objects.get(name=self.kwargs['movie_name'])
        context['reviews'] = Review.objects.filter(movie=movie)
        return context
