import re


class Review:
    def __init__(self, review_element):
        self._review_element = review_element

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
        return self._find_element_text_by_selector('review-date')[3:]

    @property
    def text(self):
        return self._find_element_text_by_selector('review-text')

    def _find_element_text_by_selector(self, selector):
        return self._review_element.find_class(selector)[0].text_content()
