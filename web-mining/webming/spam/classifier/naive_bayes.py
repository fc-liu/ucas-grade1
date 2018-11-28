import numpy as np
from .classifier import Classifier


class NaiveBayesClassifier(Classifier):
    def __init__(self, feature_map=None, label_distribution=None, label_feature=None, label_all_no=None):
        super(NaiveBayesClassifier, self).__init__()
        self.feature_map = feature_map
        self.label_distribution = label_distribution
        self.label_feature = label_feature
        self.label_all_no = label_all_no
        if self.label_distribution is not None:
            self.labels = sorted(self.label_distribution.keys())

    def save(self, filename):
        with open(filename, 'w') as out:
            out.write("%s\t%s\n" % (len(self.labels), len(self.feature_map)))
            for key, value in self.feature_map.iteritems():
                out.write("%s\t%s\n" % (key.encode('utf8'), value))
            for key, value in self.label_distribution.iteritems():
                out.write("%s\t%s\n" % (key, value))
            for key, weight in self.label_feature.iteritems():
                out.write("%s\n" % key)
                for i in xrange(weight.shape[0]):
                    out.write("%s\t%s\n" % (weight[i, 0], weight[i, 1]))
            for key, value in self.label_all_no.iteritems():
                out.write("%s\t%s\n" % (key, value))

    @staticmethod
    def load(filename):
        print(filename)
        with open(filename, 'r') as fin:
            label_num, feature_num = fin.readline().strip().split('\t')
            label_num, feature_num = int(label_num), int(feature_num)
            feature_map = dict()
            for i in range(feature_num):
                key, value = fin.readline().strip().split("\t")
                # feature_map[key.decode('utf8')] = int(value)
            label_distribution = dict()
            for i in range(label_num):
                key, value = fin.readline().strip().split("\t")
                label_distribution[int(key)] = float(value)
            label_feature = dict()
            for i in range(label_num):
                label = int(fin.readline().strip())
                weight = np.zeros((feature_num + 1, label_num))
                for j in range(feature_num + 1):
                    w1, w2 = fin.readline().strip().split('\t')
                    weight[j, 0] = float(w1)
                    weight[j, 1] = float(w2)
                label_feature[label] = weight
            label_all_no = dict()
            for i in range(label_num):
                key, value = fin.readline().strip().split('\t')
                label_all_no[int(key)] = float(value)
        return NaiveBayesClassifier(feature_map, label_distribution, label_feature, label_all_no)

    def train(self, x, y):
        self.feature_map = self.get_feature_num(x)
        self.label_distribution = self.get_label_probability(y)
        self.labels = sorted(self.label_distribution.keys())
        self.label_feature = dict()
        for label in self.labels:
            self.label_feature[label] = np.zeros((len(self.feature_map) + 1, 2))
            self.label_feature[label][:, 1] += 1
        for _x, _y in zip(x, y):
            feature_count = self.label_feature[_y]
            for feature in _x.keys():
                feature_count[self.feature_map[feature]][1] += 1
        for label in self.labels:
            label_num = self.label_distribution[label] * len(x)
            feature_count = self.label_feature[label]
            feature_count[:, 1] /= label_num
            feature_count[:, 0] = 1 - feature_count[:, 1]
        for label in self.labels:
            self.label_distribution[label] = np.log(self.label_distribution[label])
        self.label_all_no = dict()
        for label in self.labels:
            self.label_feature[label] = np.log(self.label_feature[label])
            self.label_all_no[label] = np.sum(self.label_feature[label][1:, 0])

    def classify_one(self, x):
        p_list = list()
        for label in self.labels:
            p = self.label_all_no[label] + self.label_distribution[label]
            for feature in x.keys():
                if feature in self.feature_map:
                    feature_index = self.feature_map[feature]
                    p -= self.label_feature[label][feature_index, 0]
                    p += self.label_feature[label][feature_index, 1]
            p_list.append(p)
        return np.exp(p_list[1]) / np.sum(np.exp(p_list))

    @staticmethod
    def get_label_probability(y):
        labels = dict()
        for label in y:
            if label not in labels:
                labels[label] = 1
            else:
                labels[label] += 1
        for key in labels.keys():
            labels[key] /= float(len(y))
        return labels
