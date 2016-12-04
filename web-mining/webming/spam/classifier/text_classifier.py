# encoding=utf8

# from .logistic_classify import LogisticClassifier
from .naive_bayes import NaiveBayesClassifier
import os

if __name__ == "__main__":
    nb_classifier = NaiveBayesClassifier.load("nb.bin")
    # lr_classifier = LogisticClassifier.load("lr.bin")
    text = u"感谢致电杭州萧山全金釜韩国烧烤店，本店位于金城路xxx号。韩式烧烤等，价格实惠、欢迎惠顾【全金釜韩国烧烤店】"
    # print(lr_classifier.classify_text(text))
    print(nb_classifier.classify_text(text))


def nb_classifier(email):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nb_classifier = NaiveBayesClassifier.load(os.path.join(base_dir, "classifier/nb.bin"))
    # nb_classifier = NaiveBayesClassifier.load("classifier/nb.bin")
    return nb_classifier.classify_text(email)
