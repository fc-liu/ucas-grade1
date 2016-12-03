import math
import numpy
from IOHelper import get_datalist


def build_sim_mat(data, sigma):
    n = len(data)
    sim_mat = numpy.zeros((n, n))
    for j in range(n):
        for i in range(j):
            temp_i = numpy.asarray(data[i])
            temp_j = numpy.asarray(data[j])
            temp = temp_i - temp_j
            temp = numpy.inner(temp, temp)
            temp = temp / (2 * (sigma ** 2))
            sim = temp ** math.e
            # print(temp)
            sim_mat[i, j] = sim

    sim_mat = (numpy.transpose(sim_mat) + sim_mat)

    return sim_mat


def build_degree_mat(sim_mat):
    n = len(sim_mat)
    vec = numpy.ones(n)
    D = numpy.zeros((n, n))
    for i in range(n):
        d = numpy.inner(sim_mat[i], vec)
        D[i, i] = d

    return D


def build_sys_laplace_mat(W, D):
    L = D - W
    n = len(D)
    D_2 = numpy.zeros((n, n))
    for i in range(n):
        D_2[i, i] = D[i, i] ** (-0.5)
    print("-------------------")
    print(D_2)
    L_sys = numpy.dot(numpy.dot(D_2, L), D_2)
    return L_sys

    return L


def spec_clus_Ng(sim_mat, k):
    pass


if __name__ == '__main__':
    file = "data_spec.csv"
    data = get_datalist(file)
    sigma = 1
    W = build_sim_mat(data, sigma)
    print(W)
    print("---------------------------------------")
    D = build_degree_mat(W)
    print(D)
    print("---------------------------------------")
    L = build_sys_laplace_mat(W, D)
    print(L)
