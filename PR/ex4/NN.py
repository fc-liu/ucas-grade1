import math
import numpy
from Layer import Layer
from matplotlib import pyplot as plt


class NN:
    def __init__(self):
        self.input_cells = 3
        self.hidden_cells = 7
        self.output_cells = 3
        self.w_ih = numpy.random.random(size=(self.hidden_cells, self.input_cells)) * 10
        self.w_hj = numpy.random.random(size=(self.output_cells, self.hidden_cells)) * 10
        # self.w_ih = numpy.ones((self.hidden_cells, self.input_cells)) * 5
        # self.w_hj = numpy.ones((self.output_cells, self.hidden_cells)) * 5

    def build_NN(self, sample):
        nn_sample = []
        ##initial the three layer network for every sample
        input_layer = Layer(lambda x: x, self.input_cells)
        hidden_layer = Layer(tanh, self.hidden_cells)
        output_layer = Layer(sigmoid, self.output_cells)

        # build input layer
        input_vec = sample[:3]
        input_layer.set_net_vals_from_vec(input_vec)
        input_layer.active_cells()

        # build hidden layer
        hidden_net_vec = numpy.dot(self.w_ih, input_vec)
        hidden_layer.set_net_vals_from_vec(hidden_net_vec)
        # active hidden layer cells
        hidden_layer.active_cells()
        hid_out_vec = hidden_layer.get_active_val_as_vec()

        # build output layer
        output_vec = numpy.dot(self.w_hj, hid_out_vec)
        output_layer.set_net_vals_from_vec(output_vec)

        # active output layer cells
        output_layer.active_cells()

        type = sample[3]
        base = numpy.zeros(3)
        base[type - 1] = 1
        base = numpy.asarray(base)

        nn_sample.append(input_layer)
        nn_sample.append(hidden_layer)
        nn_sample.append(output_layer)
        nn_sample.append(base)

        return nn_sample

    def BP_batch_train(self, train_data, eta, theta):
        jw_list = []
        delta_jw = 0
        while True:
            former_jw = delta_jw
            delta_w_ih = 0
            delta_w_hj = 0
            delta_jw = 0
            for sample in train_data:
                nn_sample = self.build_NN(sample)
                Z = nn_sample[2].get_active_val_as_vec()
                # net_j = nn_sample[2].get_net_val_as_vec()
                T = nn_sample[3]
                Y_T = nn_sample[1].get_active_val_as_vec()
                Y_T.shape = (Y_T.size, 1)
                Y = numpy.transpose(Y_T)
                # net_h = nn_sample[1].get_net_val_as_vec()
                X_T = nn_sample[0].get_active_val_as_vec()
                X_T.shape = (X_T.size, 1)

                sigma_j = Z * (1 - Z) * (T - Z)
                w_T = numpy.transpose(self.w_hj)
                dot = numpy.dot(w_T, sigma_j)
                sigma_h = (1 - Y ** 2) * dot
                delta_jw += self.loss_func(Z, T)
                # sigma_j.shape = (sigma_j.size, 1)
                # sigma_h.shape = (sigma_h.size, 1)
                sigma_h.shape = (1, sigma_h.size)
                sigma_j.shape = (1, sigma_j.size)
                delta_w_hj += numpy.dot(Y_T, sigma_j)
                delta_w_ih += numpy.dot(X_T, sigma_h)

            jw_list.append(delta_jw)
            # round(delta_jw, 5)
            if numpy.abs(former_jw - delta_jw) < theta:
                break
            else:
                # print("w_hj : ")
                # print(self.w_hj)
                # print("w_ih : ")
                # print(self.w_ih)
                print("Jw : ")
                print(delta_jw)
                self.w_hj += eta * delta_w_hj.transpose()
                self.w_ih += eta * delta_w_ih.transpose()
        self.plot_jw(jw_list)

    def BP_single_train(self, train_data, eta, theta):
        jw_list = []
        delta_jw = 0
        while True:
            former_jw = delta_jw
            delta_w_ih = 0
            delta_w_hj = 0
            delta_jw = 0
            for sample in train_data:
                nn_sample = self.build_NN(sample)
                Z = nn_sample[2].get_active_val_as_vec()
                # net_j = nn_sample[2].get_net_val_as_vec()
                T = nn_sample[3]
                Y_T = nn_sample[1].get_active_val_as_vec()
                Y_T.shape = (Y_T.size, 1)
                Y = numpy.transpose(Y_T)
                # net_h = nn_sample[1].get_net_val_as_vec()
                X_T = nn_sample[0].get_active_val_as_vec()
                X_T.shape = (X_T.size, 1)

                sigma_j = Z * (1 - Z) * (T - Z)
                w_T = numpy.transpose(self.w_hj)
                dot = numpy.dot(w_T, sigma_j)
                sigma_h = (1 - Y ** 2) * dot
                delta_jw += self.loss_func(Z, T)
                # sigma_j.shape = (sigma_j.size, 1)
                # sigma_h.shape = (sigma_h.size, 1)
                sigma_h.shape = (1, sigma_h.size)
                sigma_j.shape = (1, sigma_j.size)
                delta_w_hj = numpy.dot(Y_T, sigma_j)
                delta_w_ih = numpy.dot(X_T, sigma_h)
                self.w_hj += eta * delta_w_hj.transpose()
                self.w_ih += eta * 5 * delta_w_ih.transpose()

            jw_list.append(delta_jw)
            # round(delta_jw, 5)
            if numpy.abs(former_jw - delta_jw) < theta:
                break
            else:
                # print("w_hj : ")
                # print(self.w_hj)
                # print("w_ih : ")
                # print(self.w_ih)
                print("Jw : ")
                print(delta_jw)
                print("former : ")
                print(former_jw)

        self.plot_jw(jw_list)
        pass

    def plot_jw(self, jw_list):
        plt.figure(figsize=(8, 5), dpi=80)
        # axes = plt.subplot(111)
        x = numpy.arange(len(jw_list))
        plt.plot(x, jw_list, 'r.-')
        plt.xlabel('iteration times')
        plt.ylabel('aim function')
        plt.show()

    def loss_func(self, base, predict):
        if len(base) != len(predict):
            raise Exception("predict dim error")
        loss_vec = base - predict
        loss = numpy.inner(loss_vec, loss_vec)
        return loss

    def predict(self, data_vec):
        nn = self.build_NN(data_vec)
        return nn[2].get_active_val_as_vec()


def sigmoid(s):
    # print("-----------------s------------------")
    # print(s)
    s = round(s, 8)
    den = 1 + math.e ** (-s)
    frac = 1 / den

    return frac


def tanh(s):
    # print("-----------------s------------------")
    # print(s)
    s = round(s, 8)
    es = math.e ** s
    e_min_s = math.e ** (-s)

    num = es - e_min_s
    den = es + e_min_s

    frac = num / den

    return frac


if __name__ == '__main__':
    train_data = [[1.58, 2.32, -5.8, 1], [0.7, 1.58, -4.78, 1], [1.04, 1.01, -3.63, 1], [-1.49, 2.18, -3.39, 1],
                  [-0.41, 1.21, -4.73, 1], [1.39, 3.16, 2.87, 1], [1.20, 1.40, -1.89, 1], [-0.92, 1.44, -3.22, 1],
                  [0.45, 1.33, -4.38, 1], [-0.76, 0.84, -1.96, 1], [0.21, 0.03, -2.21, 2], [0.37, 0.28, -1.8, 2],
                  [0.18, 1.22, 0.16, 2], [-0.24, 0.93, -1.01, 2], [-1.18, 0.39, -0.39, 2], [0.74, 0.96, -1.16, 2],
                  [-0.38, 1.94, -0.48, 2], [0.02, 0.72, -0.17, 2], [0.44, 1.31, -0.14, 2], [0.46, 1.49, 0.68, 2],
                  [-1.54, 1.17, 0.64, 3], [5.41, 3.45, -1.33, 3], [1.55, 0.99, 2.69, 3], [1.86, 3.19, 1.51, 3],
                  [1.68, 1.79, -0.87, 3], [3.51, -0.22, -1.39, 3], [1.40, -0.44, -0.92, 3], [0.44, 0.83, 1.97, 3],
                  [0.25, 0.68, -0.99, 3], [0.66, -0.45, 0.08, 3]]
    eta = 1
    theta = 10 ** (-6)

    nn = NN()
    nn.BP_single_train(train_data, eta, theta)
