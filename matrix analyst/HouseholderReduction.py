import numpy
import math


class HouseholderReduction:
    """
        static method ,
        @:param     matrix     :   the matrix to do househoulder reduction
        @:return    (P,T)      :   A=PT, P is the orthogonal matrix,
                                    T is an upper triangular matrix
    """

    @staticmethod
    def householder_reduction(matrix):
        T = matrix.copy()
        [m, n] = T.shape
        R = numpy.identity(m)
        for i in range(n):
            if (m - i) <= 1:
                return (numpy.transpose(R), T)
            r_i = numpy.identity(m)
            length = m - i

            a_1 = T[i:, i]
            a_mod = math.sqrt(numpy.inner(a_1, a_1))
            I = numpy.identity(length)
            e = [0] * length
            e[0] = 1
            e = numpy.asarray(e)
            u = a_1 - e * a_mod
            ut = u.copy()
            u.shape = (len(u), 1)
            ut.shape = (1, len(ut))

            uut = numpy.dot(u, ut)
            utu = numpy.inner(ut, ut)[0][0]
            if utu == 0:
                return (numpy.transpose(R), T)
            om = 2 / utu * uut
            r_1 = I - 2 * numpy.dot(u, ut) / numpy.inner(ut, ut)
            r_i[i:, i:] = r_1
            R = numpy.dot(r_i, R)
            T = numpy.dot(r_i, T)

        return (numpy.transpose(R), T)
