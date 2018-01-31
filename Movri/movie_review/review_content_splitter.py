import re


class ReviewContentSplitter:
    regex = r"[.?!]"

    def __init__(self, review):
        self.review = review

    @property
    def sentences(self):
        review_sentences = re.split(self.regex, self.review.content)
        return list(filter(lambda x: len(x) > 1, review_sentences))
