import math
import numpy
from IOHelper import get_datalist
from kmeans import K_Means
from matplotlib import pyplot as plt


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
    # print("-------------------")
    # print(D_2)
    L_sys = numpy.dot(numpy.dot(D_2, L), D_2)
    return L_sys

    return L


def get_K_eigVec_as_mat(mat, k):
    (a, b) = numpy.linalg.eig(mat)
    # print("a : ")
    # print(a)
    # print("---------------------------------------")
    return b[:, :k]


def norm_row_mat(L):
    mat = L.copy()
    n = len(mat)
    for i in range(n):
        row = mat[i, :]
        norm = math.sqrt(numpy.inner(row, row))
        mat[i, :] = row / norm

    return mat


def spec_clus_Ng(data, k, sigma):
    W = build_sim_mat(data, sigma)
    # print(W)
    # print("---------------------------------------")
    D = build_degree_mat(W)
    # print(D)
    # print("---------------------------------------")
    L = build_sys_laplace_mat(W, D)
    # print(L)
    # print("---------------------------------------")
    U = get_K_eigVec_as_mat(L, k)
    # print(U)
    # print("---------------------------------------")

    T = norm_row_mat(U)

    ## plot
    # plt.figure(figsize=(8, 5), dpi=80)
    # axes = plt.subplot(111)
    # type1 = axes.scatter(T[:, 0], T[:, 1], c="red")
    # plt.show()

    # print(T)
    # print("---------------------------------------")
    mu = numpy.random.random((2, k))

    # mu = [[-0.9, 1], [-0.8, -1]]

    print("mu : ")
    print(mu)
    print("------------------")
    kmeans = K_Means()
    res = kmeans.k_means_train(T, 2, mu)
    # print(res)
    print(res)
    pass


if __name__ == '__main__':
    file = "data_spec.csv"
    data = get_datalist(file)
    sigma = 1
    k = 3
    spec_clus_Ng(data, k, sigma)
