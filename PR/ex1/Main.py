import numpy
import math
from sklearn.decomposition import PCA
from ImgHelper import Img


class pattern:
    def __init__(self):
        self.ldf_mu = []
        self.qdf_mu = []
        self.ldf_sigma = []
        self.qdf_sigma = []
        self.imgs = []
        self.ldf_imgs = []
        self.qdf_imgs = []
        self.__sum = 0
        self.amount = 0
        self.ldf_wi = 0
        self.ldf_wi0 = 0
        self.qdf_Wi = 0
        self.qdf_wi = 0
        self.qdf_wi0 = 0

        self.p = 0
        self.ldf_pca_x = None
        self.qdf_pca_x = None

    def train_ldf_par(self, total, sigma, pca_x):
        self.amount = self.imgs.__len__()
        self.p = self.amount / total
        self.ldf_pca_x = pca_x
        self.ldf_imgs = self.ldf_pca_x.transform(self.imgs)  # n*70
        self.ldf_sigma = sigma
        sigma_inv = numpy.linalg.inv(self.ldf_sigma)
        self.ldf_mu = numpy.mean(self.ldf_imgs, 0)
        self.ldf_wi = numpy.dot(sigma_inv, self.ldf_mu)
        self.ldf_wi0 = -1 / 2 * numpy.dot(numpy.dot(numpy.transpose(self.ldf_mu), sigma_inv), self.ldf_mu) + math.log(
            self.p)

        print("sigma : ")
        print(numpy.size(self.ldf_sigma))
        print("mu : ")
        print(numpy.size(self.ldf_mu))

    def train_qdf_par(self, total, pca_x):
        self.qdf_pca_x = pca_x
        self.qdf_imgs = self.qdf_pca_x.transform(self.imgs)
        self.qdf_sigma = numpy.cov(numpy.transpose(self.qdf_imgs))
        self.qdf_mu = numpy.mean(self.qdf_imgs, 0)
        sigma_inv = numpy.linalg.inv(self.qdf_sigma)
        self.qdf_Wi = -1 / 2 * sigma_inv
        self.qdf_wi = numpy.dot(sigma_inv, self.qdf_mu)
        self.qdf_wi0 = -1 / 2 * numpy.dot(numpy.dot(numpy.transpose(self.qdf_mu), sigma_inv), self.qdf_mu) + math.log(
            self.p) - 1 / 2 * math.log(
            numpy.linalg.det(self.qdf_sigma))

        print("sigma : ")
        print(numpy.size(self.qdf_sigma))
        print("mu : ")
        print(numpy.size(self.qdf_mu))

    def ldf_gx(self, img):
        img = self.ldf_pca_x.transform(img)
        return numpy.dot(img, self.ldf_wi) + self.ldf_wi0

    def qdf_gx(self, img):
        img = self.qdf_pca_x.transform(img)
        return numpy.dot(numpy.dot(img, self.qdf_Wi), numpy.transpose(img)) + numpy.dot(img, self.qdf_wi) + self.qdf_wi0


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
        self.class_num = 10
        self.total_img = []
        self.__start()

    def __start(self):
        img = Img(self.train_img, self.train_label)
        img_item = img.next_img()
        total = img.amount
        while img_item:
            if img_item[1] < 10 and img_item[1] >= 0:
                self.patterns[img_item[1]].imgs.append(img_item[0])
                self.total_img.append(img_item[0])
            img_item = img.next_img()

        pca = PCA(50)
        pca_x = pca.fit(self.total_img)

        self.total_img = pca_x.transform(self.total_img)
        cov = numpy.cov(numpy.transpose(self.total_img))
        for p in self.patterns:
            p.train_ldf_par(total, cov, pca_x)
            p.train_qdf_par(total, pca_x)

    def ldf_test(self):
        correct = 0
        error = 0
        p_correct = 0

        test_img = Img(self.test_img, self.test_label)
        test = test_img.next_img()
        while test:
            max_class = 0
            max_g = self.patterns[0].ldf_gx(test[0])
            for i in range(1, self.class_num):
                temp = self.patterns[i].ldf_gx(test[0])
                # print("temp gx for " + str(i) + " is ： ")
                # print(temp)
                if temp > max_g:
                    max_g = temp
                    max_class = i

            print("predict : ")
            print(max_class)
            print("true : ")
            print(test[1])
            if test[1] == max_class:
                correct += 1
            else:
                error += 1
            test = test_img.next_img()
        p_correct = correct / (correct + error)
        test_img.close()
        return p_correct

    def qdf_test(self):
        correct = 0
        error = 0
        p_correct = 0

        test_img = Img(self.test_img, self.test_label)
        test = test_img.next_img()
        while test:
            max_class = 0
            max_g = self.patterns[0].qdf_gx(test[0])
            for i in range(1, self.class_num):
                temp = self.patterns[i].qdf_gx(test[0])
                # print("temp gx for " + str(i) + " is ： ")
                # print(temp)
                if temp > max_g:
                    max_g = temp
                    max_class = i

            print("predict : ")
            print(max_class)
            print("true : ")
            print(test[1])
            if test[1] == max_class:
                correct += 1
            else:
                error += 1
            test = test_img.next_img()
        p_correct = correct / (correct + error)
        test_img.close()
        return p_correct


if __name__ == '__main__':
    m = Main("train-images.idx3-ubyte", "train-labels.idx1-ubyte",
             "t10k-images.idx3-ubyte", "t10k-labels.idx1-ubyte")
    ldf_correct = m.ldf_test()
    qdf_correct = m.qdf_test()
    print("ldf correct : ")
    print(ldf_correct)
    print("qdf correct : ")
    print(qdf_correct)
