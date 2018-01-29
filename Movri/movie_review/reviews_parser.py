import requests
from lxml import html

from .review import Review


class ReviewParser:
    def __init__(self, asin):
        self._asin = asin

    @property
    def reviews_url(self):
        AMAZON_DOMAIN = 'https://www.amazon.co.uk/'
        SORT_OPTION = 'sortBy=recent'
        return AMAZON_DOMAIN + 'reviews/' + self._asin + '/ref=cm_cr_arp_d_viewopt_srt?' + SORT_OPTION

    def _get_reviews_per_page_html(self, page_number):
        page_number_url = self.reviews_url + '&pageNumber=' + str(page_number)
        page = requests.get(page_number_url)
        raw_page_text = page.content

        page_tree = html.fromstring(raw_page_text)
        reviews_list_element = page_tree.get_element_by_id('cm_cr-review_list')
        reviews_list = reviews_list_element.getchildren()
        review_objects = []
        for review_element in reviews_list:
            review_objects.append(Review(review_element))

        return review_objects

    def get_most_recent_50_reviews(self):
        reviews = []
        for i in range(1, 6):
            reviews_per_day = self._get_reviews_per_page_html(page_number=i)
            reviews.extend(reviews_per_day)
        return reviews
