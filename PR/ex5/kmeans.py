import numpy
from IOHelper import get_datalist
from matplotlib import pyplot as plt


class K_Means:
    def __init__(self):
        self.c = 0
        self.mu_array = []

    def k_means_train(self, data_set, c, mu_list):
        self.c = c
        self.mu_array = mu_list

        train_data = data_set.copy()

        ## initial check
        if train_data == None or len(train_data) < 1:
            raise Exception("no train data")
        if mu_list == None or len(mu_list) < 1:
            raise Exception("no initial mu")

        dim_data = len(train_data[0])
        dim_mu = len(mu_list[0])
        if dim_data != dim_mu:
            raise Exception("data dim mismatch mu dim")

        ## begin algorithm
        isChange = True
        class_data = [[]] * self.c
        class_data[0] = train_data
        # k = 0
        while isChange:
            isChange = False
            temp_data = []
            for i in range(self.c):
                temp_data.append([])

            for i in range(class_data.__len__()):
                # print("-----------------------------------")
                # print(i)
                # k = 0
                for sample in class_data[i]:
                    index = self.classify(sample)
                    if index != i:
                        isChange = True
                    temp_data[index].append(sample)
                    # print("index : " + str(index))
                    # k += 1
                    # print(" k : " + str(k))

            for i in range(temp_data.__len__()):
                self.mu_array[i] = self.mean(temp_data[i])

            class_data = temp_data

        plot_point(class_data)

        type_list = []
        k = 0
        for sample in data_set:
            sample = numpy.asarray(sample)
            for i in range(len(class_data)):
                # print(sample)
                # print(class_data[i])
                temp = class_data[i][0]
                if not (sample - temp).all():
                    print("---------------------equal------------------")

                # class_data[i]=
                if not (sample - class_data[i]).all():
                    k += 1
                    print("k : " + str(k))
                    type_list.append(i)
                break

        for i in range(len(class_data)):
            print("amount of class " + str(i) + " is " + str(len(class_data[i])))
        self.mu_array = numpy.asarray(self.mu_array)

        return type_list

    def mean(self, data):
        data = numpy.asarray(data)
        return numpy.mean(data, axis=0)

    def classify(self, data):
        sample = data.copy()
        self.mu_array = numpy.asarray(self.mu_array)
        if type(sample) == numpy.ndarray:
            sample = sample.tolist()
        sample = sample * self.c
        length = sample.__len__()
        sample = numpy.asarray(sample).reshape(self.c, round(length / self.c))
        diff = sample - self.mu_array
        mu = []
        for i in range(len(diff)):
            vec = diff[i]
            mu.append(numpy.inner(vec, vec))

        return numpy.argmin(mu)


def plot_point(data_set):
    plt.figure(figsize=(8, 5), dpi=80)
    axes = plt.subplot(111)
    data_set = numpy.asarray(data_set)

    # x0 = data_set[:, 0]
    # y0 = data_set[:, 1]

    x0 = numpy.asarray(data_set[0])[:, 0]
    y0 = numpy.asarray(data_set[0])[:, 1]

    x1 = numpy.asarray(data_set[1])[:, 0]
    y1 = numpy.asarray(data_set[1])[:, 1]

    x2 = numpy.asarray(data_set[2])[:, 0]
    y2 = numpy.asarray(data_set[2])[:, 1]

    x3 = numpy.asarray(data_set[3])[:, 0]
    y3 = numpy.asarray(data_set[3])[:, 1]

    x4 = numpy.asarray(data_set[4])[:, 0]
    y4 = numpy.asarray(data_set[4])[:, 1]
    type1 = axes.scatter(x0, y0, c="red")
    type2 = axes.scatter(x1, y1, c="green")
    type3 = axes.scatter(x2, y2, c="blue")
    type4 = axes.scatter(x3, y3, c="yellow")
    type5 = axes.scatter(x4, y4, c="gray")
    axes.legend((type1, type2, type3, type4, type5), ("w1", "w2", "w3", "w4", "w5"), loc=2)
    # axes.legend((type1,), ("w1",), loc=2)

    plt.show()


if __name__ == '__main__':
    k = K_Means()
    file = "data.csv"
    data = get_datalist(file)
    # plot_point(data)
    c = 5
    dim = len(data[0])
    actual_mu = [[5.5, -4.5], [9, 0], [1, 4], [6.5, 4.5], [1, -1]]
    # mu = [[0, -2], [0, 5], [8, 10], [6, -10], [14, 0]]
    # mu = [[8, 1], [-2, -1], [2, 6], [4, 5], [6, 6]]
    mu = [[6, 0], [-4, 10], [-4, -8], [5, 1], [12, 0]]
    type = k.k_means_train(data, c, mu)
    print(k.mu_array)
    # print(type)
    # print(len(type))


    # mu = [[0, -2], [0, 5], [8, 10], [6, -10], [14, 0]]
    # class 0 is 192
    # class 1 is 186
    # class 2 is 216
    # class 3 is 204
    # class 4 is 202


    # result:
    # [[ 0 -1]
    #  [ 0  4]
    #  [ 5  4]
    #  [ 5 -4]
    #  [ 8  0]]



    # mu = [[8, 1], [-2, -1], [2, 6], [4, 5], [6, 6]]
    # class 0 is 378
    # class 1 is 195
    # class 2 is 109
    # class 3 is 94
    # class 4 is 224
    #
    # [[7 - 2]
    #  [0 - 1]
    #  [0  4]
    # [1
    # 3]
    # [6  4]]


    # mu=[[6, 0], [-4,10], [-4,-8], [5,1], [12,0]]
    # amount of class 0 is 204
    # amount of class 1 is 186
    # amount of class 2 is 192
    # amount of class 3 is 216
    # amount of class 4 is 202
    # [[ 5 -4]
    #  [ 0  4]
    #  [ 0 -1]
    #  [ 5  4]
    #  [ 8  0]]
