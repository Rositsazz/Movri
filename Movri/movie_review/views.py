from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from gensim.summarization import summarize

from movie_review.forms import SearchForm
from movie_review.models import Movie, Review
from movie_review.amazon_api_utils import (AmazonAPIRequest,
                                           MovieDoesNotExistException)
from movie_review.reviews_parser import ReviewParser
from movie_review.review_content_splitter import ReviewContentSplitter
from movie_review.sentence_classifier import SentenceClassifier


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
        movie, created = Movie.objects.get_or_create(name=name.strip().lower())
        if created:
            try:
                amazon_api = AmazonAPIRequest()
                movie_data = amazon_api.send_request(movie_name=name)
                movie.asin = movie_data.asin
                movie.name = movie_data.title.lower().split("[")[0].strip()
                movie.reviews_url = movie_data.reviews[1]
                movie.save()
                parser = ReviewParser(asin=movie.asin, name=movie.name)
                most_recent_reviews = parser.most_recent_reviews(
                    number_of_reviews=300)
                parser.create_review_objects(most_recent_reviews)
            except MovieDoesNotExistException:
                print('THE MOVIE DOES NOT EXIST')
        if movie.name == self.kwargs['movie_name'].lower():
            self.kwargs["movie_name"] = movie.name

        return super().form_valid(form)


class MovieReviewsView(TemplateView):
    template_name = 'movie_reviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = self.kwargs['movie_name'].title()
        movie = Movie.objects.filter(name__contains=self.kwargs['movie_name'].lower())[0]
        # movie = Movie.objects.get(name=self.kwargs['movie_name'].lower())
        if movie.positive_reviews not in ['', None]:
            context['positive_summary'] = movie.positive_reviews
            context['negative_summary'] = movie.negative_reviews
        else:

            reviews = Review.objects.filter(movie=movie)
            all_sentences = self._get_reviews_sentences(reviews)
            sentence_classifier = SentenceClassifier(all_sentences)
            context['positive_sentences'] = sentence_classifier.positive
            context['negative_sentences'] = sentence_classifier.negative
            context['positive_summary'] = summarize(" ".join(
                sentence_classifier.positive_raw_string), ratio=0.05)
            context['negative_summary'] = summarize(" ".join(
                sentence_classifier.negative_raw_string), ratio=0.05)
            movie.positive_reviews = context['positive_summary']
            movie.negative_reviews = context['negative_summary']
            movie.save()
        return context

    def _get_reviews_sentences(self, reviews):
        result = []
        for r in reviews:
            result.extend(ReviewContentSplitter(r).sentences)
        return result
