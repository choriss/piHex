import math
import gmpy2
from gmpy2 import mpz
import time
import sys


def piglgm(digits):
    errdig = 8
    precdig = digits + errdig
    base = mpz(10) ** mpz(precdig)
    gerr = mpz(10) ** mpz(errdig)
#    a = int(1. * base)
    a = base
#    b = int(1. / math.sqrt(2) * base)
    b = gmpy2.isqrt(base * base // 2)
#    t = int(1. / 4. * base)
    t = base // 4
    p = mpz(1)
    while True:
        an = (a + b) // 2
        b = gmpy2.isqrt(a * b)
        tt = a - an
        terr = tt * tt // base * p
        p = p << 1
        a = an
        print(gmpy2.num_digits(terr), end = ' \r', file = sys.stderr)
        if terr < gerr:
            break
    pi = a + b
    pi = pi * pi // t // 4
    return pi


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage:', sys.argv[0], 'DIGITS')
        sys.exit(1)
    digits = int(sys.argv[1])
    start = time.time()
    pi = piglgm(digits)
    etime = time.time() - start
    print('elapsed time:', etime, '[sec]')

    if '3.11' <= sys.version:
        sys.set_int_max_str_digits(digits + 10)
    print(pi)
#    print(str(pi)[:-4])
