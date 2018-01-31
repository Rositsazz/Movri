from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from py_thesaurus import Thesaurus
import json


# from gensim.summarization import summarize
#
# text = """
# Spoiler Alert.
# If I were Fassbender I'd kiss myself too.
# There is no sense to be made of the actions or inactions of all the characters--sort of Alien bits taken here and there and just thrown together.
# OK.
# Not as good as previous films.
# Quality and delivery fine but the film was a let down.
# Perhaps better than Prometheus but not a patch on the early films.
# I didn't think there could be three flops on the trot but I was wrong.
# """
# print(summarize(text, ratio=0.5))

# with open('train_data.json', 'r') as fp:
#     cl = NaiveBayesClassifier(fp, format="json")
# with open('train_data.json', 'r+') as f:
#     cl = NaiveBayesClassifier(f, format="json")
#
#     new_data = [("It was a torture to watch", "neg")]
#     cl.update(new_data)
#
#     dict_str = ",\n".join([str("{\"text\":\"" + str(el[0]) + "\", \"label\":\"" + str(el[1])+ "\"}") for el in cl.train_set])
#     f.seek(0)
#     f.truncate()
#     f.write("[" + dict_str + "]")

# prob_dist = cl.prob_classify("I did like it")
# print(prob_dist)
# print(prob_dist.max())
# print(round(prob_dist.prob("pos"), 2))
# print(round(prob_dist.prob("neg"), 2))
# review = """A definite drop in quality, doesn't bode well for the final season. """
wiki = TextBlob('Great')
print(wiki.sentiment)
                # classifier=cl)
# wiki = TextBlob(review, classifier=cl)
#
# print(wiki.classify())
# new_data = []
# l = Thesaurus('love')
# print(l.get_synonym())
# for tag in wiki.tags:
#     if tag[1] in ['VB']:
#         print(tag[0])
#         if cl.prob_classify(tag[0]).max() == "pos":
#             label = "pos"
#         else:
#             label = "neg"
#         new_instance = Thesaurus(tag[0])
#         synonyms = new_instance.get_synonym()
#         for syn in synonyms:
#             new_data.append((syn, label))
        # print(synonyms)
# print(wiki.tags)
# print(new_data)

# cl.update(new_data)
