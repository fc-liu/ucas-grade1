import numpy
import math
from sklearn.decomposition import PCA
from ImgHelper import Img


class Main:
    def __init__(self, k, train_img, train_label, test_img, test_label):
        self.train_img = []
        self.train_img_path = train_img
        self.train_label = train_label
        self.test_img = test_img
        self.test_label = test_label
        self.K = k

        img = Img(self.train_img_path, self.train_label)
        img_item = img.next_img()
        total = img.amount
        while img_item:
            if img_item[1] < 10 and img_item[1] >= 0:
                self.train_img.append(img_item)
            img_item = img.next_img()

    """
    through KNN to judge the class
    """

    def get_class(self, knn):
        pattern_dic = {}
        for nn in knn:
            if nn[1] in pattern_dic:
                pattern_dic[nn[1]] += 1
            else:
                pattern_dic[nn[1]] = 1
        c = None
        freq = 0
        for (k, v) in pattern_dic.items():
            if c is None:
                c = k
                freq = v
                continue
            if v > freq:
                freq = v
                c = k

        return c

    """
    find K nearest neighbors of point and return
    """

    def find_KNN(self, point):
        k = self.K
        temp_img = []
        ##initial k to temp_img
        # for i in range(k):
        #     temp = self.train_img[i]
        #     d = self.distance(point, temp)
        #     temp[2] = d
        #     temp_img.append(temp)
        # temp_img.sort(key=lambda x: x[2])
        # find K NN
        for i in range(k):
            for img in self.train_img:
                d = self.distance(img, point)
                img[2] = d
                if temp_img.__len__()<k:
                    temp_img.append(img)
                    temp_img.sort(key=lambda x: x[2])
                    continue
                if d < temp_img[k - 1][2]:
                    temp_img[k - 1] = img
                    temp_img.sort(key=lambda x: x[2])

        return temp_img

    """
    calculate distance between point x1 and x2
    """

    def distance(self, x1, x2):
        d = 0
        dim = len(x1[0])
        diff_vec = x2[0] - x1[0]
        d = diff_vec.dot(diff_vec)
        return d

    """
    test the test set and return correction
    """

    def test(self):
        correct = 0
        error = 0

        test_img = Img(self.test_img, self.test_label)
        test = test_img.next_img()
        while test:
            knn = self.find_KNN(test)
            nn_class = self.get_class(knn)

            print("predict : ")
            print(nn_class)
            print("true : ")
            print(test[1])
            if test[1] == nn_class:
                correct += 1
            else:
                error += 1
            test = test_img.next_img()

        p_correct = correct / (correct + error)
        test_img.close()
        return p_correct


if __name__ == '__main__':
    m = Main(3, "../train-images.idx3-ubyte", "../train-labels.idx1-ubyte",
             "../t10k-images.idx3-ubyte", "../t10k-labels.idx1-ubyte")
    correct = m.test()
    print("knn correct : ")
    print(correct)
