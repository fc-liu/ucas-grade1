import numpy

if __name__ == '__main__':
    A = [[1, 3, 1, -4], [-1, -3, 1, 0], [2, 6, 2, -8]]
    At = numpy.transpose(A)
    ata = numpy.dot(At, A)
    aat = numpy.dot(A, At)
    print("ATA : ")
    print(ata)
    print("A : ")
    print(A)
    print("AAT : ")
    print(aat)
