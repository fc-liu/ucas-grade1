import math
import numpy
import time

'''
README:
input is two file : mat_A and mat_B,
every file is written in the form of n*n numbers with whitespace between numbers

in my view, code is the best comment ^_^, though I added a little comment for every method
'''

'''
the strassen algorithm for matrix multiplication
'''


def strassen_mul(matrix_A, matrix_B, n):
    app_n = find_least_square(n);
    if app_n != n:
        matrix_A = append_matrix(matrix_A, n)  # append A to a 2^a*2^a matrix
        matrix_B = append_matrix(matrix_B, n)  # append A to a 2^a*2^a matrix

    c = matrix_mulp(matrix_A, matrix_B, app_n)
    sub = app_n - n
    if sub > 0:
        c = c[0:n, 0:n]
    return c


def matrix_mulp(matrix_A_app, matrix_B_app, n):
    if 1 == n:
        return matrix_A_app[0, 0] * matrix_B_app[0, 0]

    app_n = find_least_square(n)

    a11 = matrix_A_app[0:(int)(app_n / 2), 0:(int)(app_n / 2)]
    a12 = matrix_A_app[0:(int)(app_n / 2), (int)(app_n / 2):]
    a21 = matrix_A_app[(int)(app_n / 2):, 0:(int)(app_n / 2)]
    a22 = matrix_A_app[(int)(app_n / 2):, (int)(app_n / 2):]
    b11 = matrix_B_app[0:(int)(app_n / 2), 0:(int)(app_n / 2)]
    b12 = matrix_B_app[0:(int)(app_n / 2), (int)(app_n / 2):]
    b21 = matrix_B_app[(int)(app_n / 2):, 0:(int)(app_n / 2)]
    b22 = matrix_B_app[(int)(app_n / 2):, (int)(app_n / 2):]

    sub_n = int(app_n / 2)
    p1 = matrix_mulp(a11, (b12 - b22), sub_n)
    p2 = matrix_mulp((a11 + a12), b22, sub_n)
    p3 = matrix_mulp((a21 + a22), b11, sub_n)
    p4 = matrix_mulp(a22, (b21 - b11), sub_n)
    p5 = matrix_mulp((a11 + a22), (b11 + b22), sub_n)
    p6 = matrix_mulp((a12 - a22), (b21 + b22), sub_n)
    p7 = matrix_mulp((a11 - a21), (b11 + b12), sub_n)

    c11 = p4 + p5 + p6 - p2
    c12 = p1 + p2
    c21 = p3 + p4
    c22 = p1 + p5 - p3 - p7

    c1 = numpy.hstack((c11, c12))
    c2 = numpy.hstack((c21, c22))
    c = numpy.vstack((c1, c2))  # c is the result matrix of the multiplication

    return c


def grade_school_mat_mul(matrix_A, matrix_B, n):
    c = numpy.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c[i, j] += matrix_A[i, k] * matrix_B[k, j]
    return c


'''
find the least 2^a number larger than n, n is the dimension of the matrix
'''


def find_least_square(n):
    return int(math.pow(2, math.ceil(math.log2(n))))


'''
append the matrix to dimension n1, where n1 is the least 2^a number larger than n
'''


def append_matrix(matrix, n):
    append_n = int(find_least_square(n))
    # print("append_n ： " + str(append_n) + " n : " + str(n))
    if append_n == n:
        return matrix
    col = numpy.zeros((n, append_n - n))
    row = numpy.zeros((append_n - n, append_n))
    # print("col : " + str(col))
    # print("row : " + str(row))
    matrix_app = numpy.hstack((matrix, col))
    matrix_app = numpy.vstack((matrix_app, row))
    return matrix_app


'''
get matrix from file
'''


def mat_from_file(file_name):
    mat = []
    f = open(file_name)
    line = f.readline()
    while line:
        row = line.split(" ")
        if row.__len__() > 0:
            temp = []
            for cha in row:
                temp.append(int(cha))
            mat.append(temp)
        line = f.readline()
    return mat


if __name__ == '__main__':
    a = numpy.arange(1000 * 1000).reshape(1000, 1000)
    b = numpy.arange(1000 * 1000).reshape(1000, 1000)
    # a = numpy.arange(16).reshape(4, 4)
    # b = numpy.arange(16).reshape(4, 4)
    # a = numpy.eye(64)
    # b = numpy.eye(64)
    # a = mat_from_file("mat_A")
    # b = mat_from_file("mat_B")
    n = numpy.shape(a)
    # c = strassen_mul(a, b, n[0])
    start = time.clock()
    c = grade_school_mat_mul(a, b, n[0])
    end = time.clock()
    print("time for grade school : " + str(end - start))
    start = time.clock()
    c = strassen_mul(a, b, n[0])
    end = time.clock()
    print("time for strassen : " + str(end - start))
    print(c)
