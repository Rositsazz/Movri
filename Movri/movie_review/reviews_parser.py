import re
import requests
from lxml import html

class Review:
    def __init__(self, review_element):
        self._review_element = review_element

    @property
    def author(self):
        return self._review_element.find_class('author')[0].text_content()

    @property
    def rating(self):
        str_rating = self._review_element.find_class('a-icon-alt')[0].text_content()
        splitted_str_rating = re.split('([0-9]\.[0.9])', str_rating)
        return float(splitted_str_rating[1])

    @property
    def date(self):
        return review_element.find_class('review-date')[0].text_content()[3:]

    @property
    def text(self):
        return review_element.find_class('review-text')[0].text_content()


class ReviewParser:
    def __init__(self, asin):
        self._asin = asin

    @property
    def reviews_url(self):
        AMAZON_DOMAIN = 'https://www.amazon.co.uk/'
        SORT_OPTION = 'sortBy=recent'
        return AMAZON_DOMAIN + 'reviews/' + self._asin +'/ref=cm_cr_arp_d_viewopt_srt?' + SORT_OPTION


    def _get_reviews_per_page_html(self, page_number):
        page_number_url = self.reviews_url + '&pageNumber=' + str(page_number)
        page = requests.get(page_number_url)
        raw_page_text = page.content

        page_tree = html.fromstring(raw_page_text)
        import ipdb; ipdb.set_trace()
        reviews_list_element = page_tree.get_element_by_id('cm_cr-review_list')
        reviews_list = reviews_list_element.getchildren()
        review_objects = []
        for review_element in reviews_list:
            review_text = review_element.find_class('review-text')[0].text_content()
            review = Review(review_element)
            review_objects.append(review)
        import ipdb; ipdb.set_trace()

        return review_objects

    def get_most_recent_50_reviews(self):
        reviews = []
        for i in range(1,6):
            reviews_per_day = self._get_reviews_per_page_html(page_number=i)
            reviews.extend(reviews_per_day)
        return reviews

def main():
    parser = ReviewParser(asin='xxx')
    print(parser.reviews_url)
    reviews = parser.get_most_recent_50_reviews()

if __name__ == '__main__':
    main()
