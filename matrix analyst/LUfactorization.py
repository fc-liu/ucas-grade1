import numpy
from numpy.random import random

'''
class to implement PA=LU factorization
'''


class LUFactorization:
    def __init__(self, matrix):
        self.__A = matrix
        self.__rows = numpy.size(matrix, 0)
        self.__cols = numpy.size(matrix, 1)
        if self.__cols != self.__rows:
            raise Exception("A can not do LU factorization")

        self.__Ap = self.__augement_matix()
        self.__P = numpy.zeros((self.__rows, self.__rows))
        self.__L = numpy.eye(self.__rows)
        self.__U = numpy.zeros((self.__rows, self.__rows))
        self.__Ap = self.__Ap.astype(float)

    '''
    do PA=LU factorization
    '''

    def LU_facctorization_with_P(self):

        for i in range(0, self.__rows):
            # find max pivot
            pivot = i
            for j in range(i, self.__rows):
                if numpy.fabs(self.__Ap[j, i]) > numpy.fabs(self.__Ap[pivot, i]):
                    pivot = j
            if pivot != i:
                self.__row_extrange(i, pivot)

            # do the type 3 trsform
            for j in range(i + 1, self.__rows):
                mul = self.__Ap[j, i] / self.__Ap[i, i]
                mul = -mul
                self.__row_induction(i, j, mul)
                self.__Ap[j, i] = (-mul)

                # print("AP : ")
                # print(self.__Ap)

        for i in range(0, self.__rows):
            # build U
            for j in range(i, self.__rows):
                self.__U[i, j] = self.__Ap[i, j]

            # build L
            for j in range(0, i):
                self.__L[i, j] = self.__Ap[i, j]

        # build P
        for j in range(0, self.__cols):
            val = int(self.__Ap[j, self.__cols])
            self.__P[j, val - 1] = 1
        return (self.__P, self.__L, self.__U)

    '''
    build an augemented matrix
    '''

    def __augement_matix(self):
        p = numpy.arange(1, self.__rows + 1).reshape(self.__rows, 1)
        return numpy.hstack((self.__A, p))

    '''
    exchange two rows of the augemented matrix
    '''

    def __row_extrange(self, row1, row2):
        for i in range(0, self.__cols + 1):
            temp = self.__Ap[row1, i]
            self.__Ap[row1, i] = self.__Ap[row2, i]
            self.__Ap[row2, i] = temp
            # if i<self.__cols:
            #     temp_l = self.__L[row1, i]
            #     self.__L[row1, i] = self.__L[row2, i]
            #     self.__L[row2, i] = temp_l

    '''
    rows induction, row2=row2-mul*row1
    '''

    def __row_induction(self, row1, row2, mul):
        for i in range(row1, self.__cols):
            self.__Ap[row2, i] += self.__Ap[row1, i] * mul
