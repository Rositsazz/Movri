from textblob.classifiers import NaiveBayesClassifier


class NBClassifier:
    def __init__(self, train_data_file):
        self._train_data_file = train_data_file
        f = open(self._train_data_file, 'r+')
        self._cl = NaiveBayesClassifier(f, format="json")
        f.close()

    def update_train_set(self, sentence):
        new_data = [(sentence.str_sentence, sentence.label)]
        self._cl.update(new_data)
        self._save_data_to_file()

    def _save_data_to_file(self):
        TEXT = "{\"text\":\""
        LABEL = "\", \"label\":\""
        dict_str = ",\n".join([str(TEXT + str(el[0]) + LABEL + str(el[1])+ "\"}") for el in self._cl.train_set])
        f = open(self._train_data_file, 'r+')
        f.write("[" + dict_str + "]")
        f.close()

    def prob_classify(self, sentence):
        # import ipdb; ipdb.set_trace()
        return self._cl.prob_classify(sentence).max()
