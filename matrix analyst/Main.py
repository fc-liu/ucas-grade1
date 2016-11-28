import numpy
from LUfactorization import LUFactorization
from HouseholderReduction import HouseholderReduction
from GivensReduction import GivensReduction
from QRfactorization import QRfactorization

"""
the main entry of the matrix factorization program

@:param matrix: the matrix to be reducted

@:param mode: choose which matrix reduction :
        "LU"    :   PA=LU    LU reduction
        "QR"    :   A=QR     QR(Gram-Schmidt) reduction
        "H"     :   PA=T     Householder reduction
        "G"     :   PA=T     Givens reduction

@:return
        "LU"    :   return triple (P,L,U)
        "QR"    :   return (Q,R)    A=QR
        "H"     :   return (Q,R)    A=QR
        "G"     :   return (Q,R)    A=QR
"""


def matrix_reduction(matrix, mode):
    matrix = numpy.asarray(matrix)
    if mode == "LU" or mode == "lu":
        lu = LUFactorization(matrix)
        (p, l, u) = lu.LU_facctorization_with_P()
        return (p, l, u)
    elif mode == "QR" or mode == "qr":
        (q, r) = QRfactorization.Gram_Schmidt(matrix)
        return (q, r)
    elif mode == "H" or mode == "h":
        (q, r) = HouseholderReduction.householder_reduction(matrix)
        return (q, r)
    elif mode == "G" or mode == "g":
        (q, r) = GivensReduction.givens_reduction(matrix)
        return (q, r)


if __name__ == '__main__':
    # A = random((4, 4))
    qr = [[1, 2, -3, 4], [4, 8, 12, -8], [2, 3, 2, 1], [-3, -1, 1, -4]]
    # qr = [[0, -20, -14], [3, 27, -4], [4, 11, -2], [1, 1, 1]]
    # qr = [[1, 2, 3], [4, 5, 6]]
    # qr = [[1, 2], [3, 4], [5, 6]]

    (p, l, u) = matrix_reduction(qr, "lu")
    (q, r) = matrix_reduction(qr, "qr")
    (q_h, r_h) = matrix_reduction(qr, "h")
    (q_g, r_g) = matrix_reduction(qr, "g")

    # A = numpy.dot(q, r)
    #
    # print("A : ")
    # print(A)
    # print("QTQ : ")
    # print(numpy.dot(q, numpy.transpose(q)))

    print("LU fractorization : ")
    print("P : ")
    print(p)
    print("L : ")
    print(l)
    print("U : ")
    print(u)

    print("Gram-Schmidt : ")
    print("Q : ")
    print(q)
    print("R : ")
    print(r)

    print("Househoulder reduction : ")
    print("Q : ")
    print(q_h)
    print("R : ")
    print(r_h)

    print("Givens reduction : ")
    print("Q : ")
    print(q_g)
    print("R : ")
    print(r_g)
