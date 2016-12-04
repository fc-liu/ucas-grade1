class Classifier(object):
    def __init__(self): pass

    def train(self, data_x, data_y): pass

    def classify_one(self, x): pass

    def classify_batch(self, x):
        return [self.classify_one(_x) for _x in x]

    def classify_text(self, text):
        import jieba
        seg = {seg:1 for seg in jieba.cut(text)}
        return self.classify_one(seg)

    def save(self, filename): pass

    @staticmethod
    def load(filename): pass

    @staticmethod
    def get_feature_num(data):
        feature_map = dict()
        for instance in data:
            for key in instance.keys():
                if key not in feature_map:
                    feature_map[key] = len(feature_map) + 1
        return feature_map
