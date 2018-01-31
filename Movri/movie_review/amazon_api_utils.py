from amazon.api import AmazonAPI

class MovieDoesNotExistException(Exception):
    pass


class AmazonAPIRequest:
    AMAZON_ACCESS_KEY = ''
    AMAZON_SECRET_KEY = ''
    AMAZON_ASSOC_TAG = ''

    def __init__(self):
        self.amazon = AmazonAPI(self.AMAZON_ACCESS_KEY,
                                self.AMAZON_SECRET_KEY,
                                self.AMAZON_ASSOC_TAG,
                                region='UK')

    def send_request(self, movie_name=''):
        try:
            movie = self.amazon.search_n(1,
                                         Keywords=movie_name,
                                         SearchIndex='DVD')
        except Exception:
            raise MovieDoesNotExistException(
                'This is not a movie name - {movie_name}'.format(
                    movie_name=movie_name))

        return movie[0]
