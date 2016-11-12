import numpy
import math


class LinearDisFunc:
    def __init__(self):
        self.a = []
        self.eta = 1
        self.theta = 0

    def Ho_Kashyap_algorithm(self, train_data, a, b, eta, b_min, k_max):
        k = 0
        train_pinv = numpy.linalg.pinv(train_data)
        while k <= k_max:
            e = numpy.dot(a, numpy.transpose(train_data)) - b  # e=Ya-b
            # e = math.sqrt(numpy.inner(err_vec, err_vec))
            e_plus = (abs(e) + e) / 2
            b = b + 2 * eta * e_plus
            a = numpy.dot(b, numpy.transpose(numpy.linalg.pinv(train_data)))
            if min(e) <= b_min:
                return [a, b]
            k += 1
            print("error : " + str(e))
        print("no solution found")
        return [a, b]

    def batch_relax_with_margin(self, train_dataList, a, b, eta):
        k = 0

        while True:
            Y = []
            for sample in train_dataList:
                err = numpy.inner(a, sample) - b
                if err <= 0:
                    Y.append(sample)
            if Y.__len__() == 0:
                return a
            ak = a
            for err_sample in Y:
                y_norm = numpy.inner(err_sample, err_sample)
                err = numpy.inner(a, err_sample) - b
                ak = ak - eta * err / y_norm * err_sample
            print("a : " + str(a))
            a = ak

    def single_sample_relax_with_margin(self, train_dataList, a, b, eta):
        k = 0

        while True:
            Y = []
            for sample in train_dataList:
                err = numpy.inner(a, sample) - b
                if err <= 0:
                    Y.append(sample)
            if Y.__len__() == 0:
                return a
            for err_sample in Y:
                y_norm = numpy.inner(err_sample, err_sample)
                err = numpy.inner(a, err_sample) - b
                a = a - eta * err / y_norm * err_sample
            print("a : " + str(a))

    def batch_perception(self, train_data_list, a, eta, theta):
        Y = []
        ja = theta + 1
        iter_count = 0
        while ja > theta:
            ja = 0
            iter_count += 1
            print(iter_count)
            for err in Y:
                a = a + eta * err
            Y.clear()
            for sample in train_data_list:
                g = numpy.inner(a, sample)
                if g <= 0:
                    ja = ja + abs(eta * numpy.inner(sample, sample))
                    Y.append(sample)
            print("Ja : ")
            print(ja)
        print("iterration count ： ")
        print(iter_count)
        return a

    def norm_aug_sample(self, data_list):
        if data_list:
            norm_data = numpy.array(data_list)
            temp = norm_data[0]
            dim = len(temp)
            tag = temp[dim - 1]
            for i in range(norm_data.__len__()):
                sample = norm_data[i]
                if sample[dim - 1] != tag:
                    sample[dim - 1] = 1
                    norm_data[i] = -sample
                else:
                    sample[dim - 1] = 1
            return norm_data
        else:
            return None

    def train_batch_perception(self, train_data_list):
        norm_data = self.norm_aug_sample(train_data_list)
        dim = norm_data[0].__len__()
        self.a = numpy.zeros(dim)
        self.a = self.batch_perception(norm_data, self.a, self.eta, self.theta)
        print(norm_data)

        ja = 0
        for sample in norm_data:
            g = self.ldf(sample)
            if g < 0:
                print(sample)
                ja += 1

        print("ja : " + str(ja))

    def ldf(self, sample):
        return numpy.inner(self.a, sample)

    def train_Ho_Kashyap(self, train_data_list):
        b_min = 0.15
        k_max = 1500
        eta = 0.5

        norm_data = self.norm_aug_sample(train_data_list)
        n = norm_data.__len__()
        dim = norm_data[0].__len__()

        a = numpy.ones(dim)
        b = numpy.zeros(n) + 0.1

        ret = self.Ho_Kashyap_algorithm(norm_data, a, b, eta, b_min, k_max)
        if ret:
            a = ret[0]
            b = ret[1]
        print(norm_data)

        ja = 0
        for sample in norm_data:
            g = numpy.inner(a, sample) - b_min
            if g < 0:
                print(sample)
                ja += 1

        print("ja : " + str(ja))

    def train_batch_relax_with_margin(self, train_data_list):
        b = 0.5
        eta = 0.5

        norm_data = self.norm_aug_sample(train_data_list)
        dim = norm_data[0].__len__()

        a = numpy.zeros(dim)

        a = self.batch_relax_with_margin(norm_data, a, b, eta)
        print(norm_data)
        print(" a : " + str(a))

        ja = 0
        for sample in norm_data:
            g = numpy.inner(a, sample) - b
            if g <= 0:
                print(sample)
                ja += 1

        print("ja : " + str(ja))


if __name__ == '__main__':
    w1 = [[0.1, 1.1, 1], [6.8, 7.1, 1], [-3.5, -4.1, 1], [2.0, 2.7, 1], [4.1, 2.8, 1], [3.1, 5.0, 1], [-0.8, -1.3, 1],
          [0.9, 1.2, 1], [5.0, 6.4, 1], [3.9, 4.0, 1]]
    w2 = [[7.1, 4.2, 2], [-1.4, -4.3, 2], [4.5, 0.0, 2], [6.3, 1.6, 2], [4.2, 1.9, 2], [1.4, -3.2, 2], [2.4, -4.0, 2],
          [2.5, -6.1, 2], [8.4, 3.7, 2], [4.1, -2.2, 2]]
    w3 = [[-3.0, -2.9, 3], [0.5, 8.7, 3], [2.9, 2.1, 3], [-0.1, 5.2, 3], [-4.0, 2.2, 3], [-1.3, 3.7, 3], [-3.4, 6.2, 3],
          [-4.1, 3.4, 3], [-5.1, 1.6, 3], [1.9, 5.1, 3]]
    w4 = [[-2.0, -8.4, 4], [-8.9, 0.2, 4], [-4.2, -7.7, 4], [-8.5, -3.2, 4], [-6.7, -4.0, 4], [-0.5, -9.2, 4],
          [-5.3, -6.7, 4], [-8.7, -6.4, 4], [-7.1, -9.7, 4], [-8.0, -6.3, 4]]

    data = w1 + w3
    ldf = LinearDisFunc()
    # ldf.train_Ho_Kashyap(data)
    ldf.train_batch_relax_with_margin(data)
    print("aT : ")
    print(ldf.a)
