import numpy
import math

"""
implement of Givens reduction
"""


class GivensReduction:
    """
    static method ,
    @:param     matrix     :   the matrix to do givens reduction
    @:return    (P,T)      :   A=PT, P is the orthogonal matrix,
                                T is an upper triangular matrix
    """

    @staticmethod
    def givens_reduction(matrix):
        T = matrix.copy()
        [m, n] = T.shape
        P = numpy.identity(m)
        for i in range(min(m, n)):
            for j in range(i + 1, m):
                v_i = T[i, i]
                p_ij = numpy.identity(m)
                v_j = T[j, i]
                l = math.sqrt(v_i ** 2 + v_j ** 2)
                c = v_i / l
                s = v_j / l
                p_ij[i, i] = c
                p_ij[i, j] = s
                p_ij[j, i] = -s
                p_ij[j, j] = c
                T = numpy.dot(p_ij, T)
                P = numpy.dot(p_ij, P)

        return (numpy.transpose(P), T)
