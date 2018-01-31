from .sentence import Sentence
from .nb_classifier import NBClassifier


class SentenceClassifier:
    def __init__(self, sentence_set):
        self._sentence_set = sentence_set
        self._classifier = NBClassifier('movie_review/train_data.json')
        self._positive = []
        self._negative = []

        self._identify_sentences_label()

    @property
    def positive(self):
        return self._positive

    @property
    def negative(self):
        return self._negative

    @property
    def positive_raw_string(self):
        res = []
        for el in self._positive:
            res.append(el.str_sentence + ".")
        return res

    @property
    def negative_raw_string(self):
        res = []
        for el in self._negative:
            res.append(el.str_sentence + ".")
        return res

    def _identify_sentences_label(self):
        for str_sentence in self._sentence_set:
            sentence = Sentence(str_sentence, self._classifier)
            if sentence.label == "pos":
                self._positive.append(sentence)
            else:
                self._negative.append(sentence)

            if sentence.polarity > 0.8 or sentence.polarity < -0.6:
                self._classifier.update_train_set(sentence)
            # self._classifier.update_train_set(sentence)
