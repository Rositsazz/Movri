import re
from datetime import datetime

from .models import Movie, Review as ReviewModel


class Review:
    def __init__(self, review_element, movie_name=''):
        self._review_element = review_element
        self.movie_name = movie_name

    @property
    def author(self):
        return self._find_element_text_by_selector('author')

    @property
    def rating(self):
        str_rating = self._find_element_text_by_selector('a-icon-alt')
        splitted_str_rating = re.split('([0-9]\.[0.9])', str_rating)
        return float(splitted_str_rating[1])

    @property
    def date(self):
        str_date = self._find_element_text_by_selector('review-date')[3:]
        return datetime.strptime(str_date, '%d %B %Y').date()

    @property
    def text(self):
        return self._find_element_text_by_selector('review-text')

    def create(self):
        ReviewModel.objects.create(
            movie=Movie.objects.get(name=self.movie_name),
            content=self.text,
            author=self.author,
            date=self.date,
            rating=self.rating
        )

    def _find_element_text_by_selector(self, selector):
        return self._review_element.find_class(selector)[0].text_content()

    def __str__(self):
        return "Review: " + self.text + "\n"
