import requests
from lxml import html
from .review import Review


class ReviewParser:
    AMAZON_DOMAIN = 'https://www.amazon.co.uk/'

    def __init__(self, asin, name):
        self._asin = asin
        self._name = name

    @property
    def reviews_url(self):
        SORT_OPTION = 'sortBy=recent'
        PAGE_SIZE = 'pageSize=50'
        PARAM = '/ref=cm_cr_arp_d_viewopt_srt?' + PAGE_SIZE + '&' + SORT_OPTION
        return self.AMAZON_DOMAIN + 'reviews/' + self._asin + PARAM

    def _get_reviews_per_page_html(self, page_number):
        page_tree = self._page_tree(page_number=page_number)

        reviews_list_element = page_tree.get_element_by_id('cm_cr-review_list')

        reviews_list = reviews_list_element.getchildren()[:-1]
        review_objects = []
        for review_element in reviews_list:
            review_objects.append(Review(review_element, self._name))
        return review_objects

    def most_recent_reviews(self, number_of_reviews=50):
        number_of_pages = int(number_of_reviews/50) + 1

        page_tree = self._page_tree(page_number=1)

        reviews_count = int(page_tree.find_class(
            'totalReviewCount')[0].text_content().replace(',', ''))
        reviews_list_element = page_tree.get_element_by_id('cm_cr-review_list')
        reviews_list = reviews_list_element.getchildren()[:-1]
        review_objects = []
        for i, review_element in enumerate(reviews_list):
            if i < number_of_reviews:
                review_objects.append(Review(review_element, self._name))

        if number_of_pages > 1:
            for i in range(2, number_of_pages + 1):
                if len(review_objects) < reviews_count:
                    reviews_per_page = self._get_reviews_per_page_html(
                        page_number=i)
                    review_objects.extend(reviews_per_page)

        return review_objects

    def create_review_objects(self, reviews):
        for rev_obj in reviews:
            rev_obj.create()

    def _page_tree(self, page_number=1):
        page_url = self.reviews_url + '&pageNumber=' + str(page_number)
        page = requests.get(page_url)
        raw_page_text = page.content

        return html.fromstring(raw_page_text)
