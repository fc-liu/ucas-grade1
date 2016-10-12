import numpy
import math
from ImgHelper import Img


class pattern:
    def __init__(self):
        self.mu = []
        self.sigma = []
        self.imgs = []
        self.__sum = 0
        self.amount = 0
        self.ldf_wi = 0
        self.ldf_wi0 = 0
        self.p = 0

    def finish_append(self, total):
        self.sigma = numpy.cov(numpy.transpose(self.imgs))
        self.mu = numpy.mean(self.imgs, 0)
        self.amount = self.imgs.__len__()
        self.p = self.amount / total
        self.ldf_wi=self.mu/self.sigma
        print("sigma : ")
        print(numpy.size(self.sigma))
        print("mu : ")
        print(numpy.size(self.mu))

    def ldf(self, img):


class Main:
    def __init__(self, train_img, train_label, test_img, test_label):
        p0 = pattern()
        p1 = pattern()
        p2 = pattern()
        p3 = pattern()
        p4 = pattern()
        p5 = pattern()
        p6 = pattern()
        p7 = pattern()
        p8 = pattern()
        p9 = pattern()
        self.patterns = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
        self.train_img = train_img
        self.train_label = train_label
        self.test_img = test_img
        self.test_label = test_label
        self.start()

    def start(self):
        img = Img(self.train_img, self.train_label)
        img_item = img.next_img()
        total = img.amount
        while img_item:
            if img_item[1] < 10 and img_item[1] >= 0:
                self.patterns[img_item[1]].imgs.append(img_item[0])
            img_item = img.next_img()
        for p in self.patterns:
            p.finish_append()

        test_img = Img(self.test_img, self.test_label)
        test = test_img.next_img()
        c = self.LDF(test[0])
        print("predict : ")
        print(c)
        print("true : ")
        print(test[1])


if __name__ == '__main__':
    m = Main("train-images.idx3-ubyte", "train-labels.idx1-ubyte",
             "t10k-images.idx3-ubyte", "t10k-labels.idx1-ubyte")
    m.start()
