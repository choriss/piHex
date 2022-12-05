import math
import sys


def lmul(base, x, y):
    return x * y // base


def ldiv(base, x, y):
    return x * base // y


def lsqrt(base, a):
    x = base
    while True:
        xn = x - ldiv(base, lmul(base, x, x) - a, 2 * x)
        if -1 <= (x - xn) <= 1:
            return xn
        x = xn


def pigl(digits):
    errdig = 8
    tprecdig = digits + errdig
    if tprecdig % 8 != 0:
        assert('precdig + errdig should be multiple of 8')
    tbase  = 1 * (10 ** tprecdig)
    tbase2 = 1 * (10 ** (tprecdig // 2))
    gterr = 1 * (10 ** errdig)
#    a = int(1. * base)
    a = tbase2
#    b = int(1. / math.sqrt(2) * base)
    b = tbase2 // 2
    b = lsqrt(tbase2, b)
#    t = int(1. / 4. * base)
    t = tbase // 4
    p = tbase
    while True:
        an = (a + b) // 2
        bt = lmul(tbase2, a, b)
        b = lsqrt(tbase2, bt)
        tt = a - an
        tt = lmul(1, tt, tt)
        tt = t - lmul(tbase, p, tt)
        p = 2 * p
        a = an
        terr = abs(t - tt)
        t = tt
        if terr < gterr:
            break
    pi = a + b
    pi = lmul(1, pi, pi)
    pi = ldiv(tbase, pi, t) // 4
    return pi


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage:', sys.argv[0], 'DIGITS')
        sys.exit(1)
    digits = int(sys.argv[1])
    pi = pigl(digits)

    if '3.11' <= sys.version:
        sys.set_int_max_str_digits(digits + 10)
    print(pi)
#    print(str(pi)[:-4])
