import math
import time
import random

'''t
the Karatsuba algorithm for multiplication
'''


def Karastuba_mul(x, y):
    n = get_n(x)
    c = 0
    cut = math.ceil(n / 2)
    if n <= 1:
        c = x * y
    else:
        po = math.pow(10, cut)
        xl = x % po
        xh = (x - xl) / po
        yl = y % po
        yh = (y - yl) / po
        p = Karastuba_mul((xh + xl), (yh + yl))
        c = xh * yh * math.pow(10, 2 * cut) + (p - xh * yh - Karastuba_mul(xl, yl)) * math.pow(10, cut) + Karastuba_mul(
            xl, yl)
        # print("xl ： " + str(xl))
        # print("xh ： " + str(xh))
        # print("yl ： " + str(yl))
        # print("yh ： " + sr(yh))
        # print("p ： " + str(p))

    return c


def quadratic_mul(x, y):
    nx = get_n(x)
    ny = get_n(y)
    c = 0
    cut_x = math.ceil(nx / 2)
    cut_y = math.ceil(ny / 2)
    if nx <= 1 or ny <= 1:
        c = x * y
    else:
        po = math.pow(10, cut_x)
        xl = x % po
        xh = (x - xl) / po
        po = math.pow(10, cut_y)
        yl = y % po
        yh = (y - yl) / po
        c = xh * yh * math.pow(10, cut_x + cut_y) + (
            quadratic_mul(xh, yl) * math.pow(10, cut_x) + quadratic_mul(yh, xl) * math.pow(10, cut_y)) + Karastuba_mul(
            xl, yl)
        # print("xl ： " + str(xl))
        # print("xh ： " + str(xh))
        # print("yl ： " + str(yl))
        # print("yh ： " + sr(yh))
        # print("p ： " + str(p))

    return c


'''
get bits of a number
'''


def get_n(num):
    a = num
    n = 0
    a = (a - a % 10) / 10
    while a != 0:
        a = (a - a % 10) / 10
        n += 1
    return n


'''
main: input a=x, b=y, then call the mul method to multiple x and y
'''
if __name__ == '__main__':
    # a = 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
    # b = 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111199999999999999999999999999999999
    a = random.random() * math.pow(10, 100)
    b = random.random() * math.pow(10, 100)
    start = time.clock()
    c = Karastuba_mul(a, b)
    end = time.clock()
    print("time for karastuba : " + str(end - start) + " c : " + str(c))
    start = time.clock()
    c = quadratic_mul(a, b)
    end = time.clock()
    print("time for quadratic : " + str(end - start) + " c : " + str(c))
