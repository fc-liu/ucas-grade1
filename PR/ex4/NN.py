import math
import numpy
from Layer import Layer


class NN:
    def __init__(self):
        self.input_cells = 3
        self.hidden_cells = 4
        self.output_cells = 3
        self.w_ih = numpy.random.random(size=(self.hidden_cells, self.input_cells))
        self.w_hj = numpy.random.random(size=(self.output_cells, self.hidden_cells))

    def build_NN(self, sample):
        nn_sample = []
        ##initial the three layer network for every sample
        input_layer = Layer(lambda x: x, self.input_cells)
        hidden_layer = Layer(tanh, self.hidden_cells)
        output_layer = Layer(sigmoid, self.output_cells)

        # build input layer
        input_vec = sample[:3]
        input_layer.set_net_vals_from_vec(input_vec)

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
        base[type] = 1

        nn_sample.append(input_layer)
        nn_sample.append(hidden_layer)
        nn_sample.append(output_layer)
        nn_sample.append(base)

        return nn_sample

    def propagate(self):

    def BP_batch_train(self, train_data, eta, theta):
        while True:
            delta_w_ih = 0
            delta_w_hj = 0
            delta_jw = 0
            for sample in train_data:
                

            if numpy.abs(delta_jw) < theta:
                break

    def BP_single_train(self, train_data, eta, theta):

        pass

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
    den = 1 + math.e ** (-s)
    frac = 1 / den

    return frac


def tanh(s):
    es = math.e ** s
    e_min_s = math.e ** (-s)

    num = es - e_min_s
    den = es + e_min_s

    frac = num / den

    return frac
