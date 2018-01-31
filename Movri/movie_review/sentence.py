from textblob import TextBlob


class Sentence:
    def __init__(self, str_sentence, classifier=None):
        self.str_sentence = str_sentence
        self._classifier = classifier

    @property
    def label(self):
        return self._get_label()

    @property
    def sentiment(self):
        return TextBlob(self.str_sentence)

    @property
    def polarity(self):
        return self.sentiment.polarity

    def __str__(self):
        return self.str_sentence

    def _get_label(self):
        # import ipdb; ipdb.set_trace()
        if self.polarity >= 0.5:
            return "pos"
        elif self.polarity <= -0.5:
            return "neg"
        else:
            return self._calculate_label_based_on_training_set()

    def _calculate_label_based_on_training_set(self):
        prob_label = self._classifier.prob_classify(self.str_sentence)
        return prob_label
