import numpy
import math


class QRfactorization:
    def __init__(self):
        print("QR ")

    """
        static method ,
        @:param     matrix     :   the matrix to do Gram-schmidt factorization
        @:return    (Q,R)      :   A=QR, Q is the orthogonal matrix,
                                    R is an upper triangular matrix
    """

    @staticmethod
    def Gram_Schmidt(matrix):
        (m, n) = matrix.shape
        Q = numpy.zeros((m, n))
        R = numpy.zeros((n, n))
        a = matrix[:, 0]
        v = math.sqrt(numpy.inner(a, a))
        q = a / v
        R[0, 0] = v
        Q[:, 0] = q
        for i in range(1, n):
            a = matrix[:, i]
            q = a
            for j in range(i):
                q_j = Q[:, j]
                q = q - numpy.inner(q_j, a) * q_j
                R[j, i] = numpy.inner(q_j, a)

            v = math.sqrt(numpy.inner(q, q))
            q = q / v
            R[i, i] = v
            Q[:, i] = q

        return (Q, R)
