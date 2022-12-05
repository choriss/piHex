# https://www.4gamer.net/games/120/G012093/20130323002/
# https://xn--w6q13e505b.jp/formula/bbp.html
# http://www.kk62526.server-shared.com/pi/BBP.html

import math
import gmpy2
from gmpy2 import mpfr
from gmpy2 import mpz
from concurrent.futures import ProcessPoolExecutor as Executor
import sys

# all ...digits are 16-based (...bits are 2-based)

# digits for over calculation: carry will occur in probability of 1/16
# per digit; will make error on prob of 1/16**(overdigits).


# get 16 **a (mod b)
def exp16mod(a, b):
    p = 16
    r = 1
    while 0 < a:
        if a & 1 == 1:
            r = (r * p) % b
        p = (p * p) % b
        a >>= 1
    return r


def bbp(digstart):
    digstart = digstart - 1
    overdig = 13
    rss = 0.
    for k in range(0, digstart):
#        rs = 4. + pow(16, digstart - k, 8 * k + 1) * 4 / (8 * k + 1) -\
#                  pow(16, digstart - k, 8 * k + 4) * 2 / (8 * k + 4) -\
#                  pow(16, digstart - k, 8 * k + 5) * 1 / (8 * k + 5) -\
#                  pow(16, digstart - k, 8 * k + 6) * 1 / (8 * k + 6)
        k8 = k << 3
        rs = 4. + (pow(16, digstart - k, k8 + 1) << 2) / (k8 + 1) -\
                  (pow(16, digstart - k, k8 + 4) << 1) / (k8 + 4) -\
                  (pow(16, digstart - k, k8 + 5)     ) / (k8 + 5) -\
                  (pow(16, digstart - k, k8 + 6)     ) / (k8 + 6)
        rss += rs
        rss, _ = math.modf(rss)
#        print(k, ':', rss)
#    print('---')
    for k in range(digstart, digstart + overdig):
        rs = 16 ** (digstart - k) * (4 / (8 * k + 1) -\
                                     2 / (8 * k + 4) -\
                                     1 / (8 * k + 5) -\
                                     1 / (8 * k + 6))
        rss += rs
        rss, _ = math.modf(rss)
#        print(k, ':', rss)
    return rss


def bbpgmp(digstart, digdisp):
    digstart = digstart - 1
    overdig = digdisp + 10
    rss = mpfr(0.)
    lsum = mpfr(0.)
    ldig = [1248, 2496, 3744, 4992, 6240, 7488, 8736]
    for k in range(0, digstart):
        if k in ldig:
            print('-', k, ':', lsum)
            lsum = mpfr(0.)
#        rs = 4. + pow(16, digstart - k, 8 * k + 1) * 4 / (8 * k + 1) -\
#                  pow(16, digstart - k, 8 * k + 4) * 2 / (8 * k + 4) -\
#                  pow(16, digstart - k, 8 * k + 5) * 1 / (8 * k + 5) -\
#                  pow(16, digstart - k, 8 * k + 6) * 1 / (8 * k + 6)
        k8 = k << 3
        dk = mpz(digstart - k)
        rs = mpfr(4.) + \
                 mpfr(gmpy2.powmod(mpz(16), dk, k8 + 1) << 2) / (k8 + 1) -\
                 mpfr(gmpy2.powmod(mpz(16), dk, k8 + 4) << 1) / (k8 + 4) -\
                 mpfr(gmpy2.powmod(mpz(16), dk, k8 + 5)     ) / (k8 + 5) -\
                 mpfr(gmpy2.powmod(mpz(16), dk, k8 + 6)     ) / (k8 + 6)
        rss += rs
#        rss = rss - int(rss)
        rss = gmpy2.frac(rss)
        lsum += rs
        lsum = gmpy2.frac(lsum)
#        print(k, ':', rss)
    print(lsum)
#    print('---')
    for k in range(digstart, digstart + overdig):
        rs = 16 ** (digstart - k) * (mpfr(4.) / (8 * k + 1) -\
                                     mpfr(2.) / (8 * k + 4) -\
                                     mpfr(1.) / (8 * k + 5) -\
                                     mpfr(1.) / (8 * k + 6))
        rss += rs
        rss = gmpy2.frac(rss)
#        print(k, ':', rss)
    return rss


def bbpmpth(startk, endk, digstart, digdisp, shift, mod8):
    fpprec = len(str(digstart)) + 4 * digdisp + 20
    gmpy2.get_context().precision = fpprec
    rs = mpfr(0.)
    for k in range(startk, endk):
        k8 = k << 3
        dk = mpz(digstart - k)
        rs += mpfr(gmpy2.powmod(mpz(16), dk, k8 + mod8) << shift) / (k8 + mod8)
        rs = gmpy2.frac(rs)
    return rs


def bbpmpgmp(digstart, digdisp):
    digstart = digstart - 1
    overdig = digdisp + 10
    rss = mpfr(0.)
    digdiv = int(digstart * .45)
    futures = []
    pm = [1, -1, -1, -1, 1, -1, -1, -1]
    with Executor() as exec:
## divide process (into 8) by term (into 4) & loop count (into 2)
        futures.append(exec.submit(bbpmpth, 0, digdiv, digstart, digdisp, 2, 1))
        futures.append(exec.submit(bbpmpth, 0, digdiv, digstart, digdisp, 1, 4))
        futures.append(exec.submit(bbpmpth, 0, digdiv, digstart, digdisp, 0, 5))
        futures.append(exec.submit(bbpmpth, 0, digdiv, digstart, digdisp, 0, 6))
        futures.append(exec.submit(bbpmpth, digdiv, digstart, digstart,
                                   digdisp, 2, 1))
        futures.append(exec.submit(bbpmpth, digdiv, digstart, digstart,
                                   digdisp, 1, 4))
        futures.append(exec.submit(bbpmpth, digdiv, digstart, digstart,
                                   digdisp, 0, 5))
#        futures.append(exec.submit(bbpmpth, digdiv, digstart, digstart,
#                                   digdisp, 0, 6))
        print('start future #0-', len(futures))
        rs = bbpmpth(digdiv, digstart, digstart, digdisp, 0, 6)
#
## divide process (into 4) by term
#        futures.append(exec.submit(bbpmpth, 0, digstart, digstart, digdisp,
#                                   2, 1))
#        pm.append(1)
#        futures.append(exec.submit(bbpmpth, 0, digstart, digstart, digdisp,
#                                   1, 4))
#        pm.append(-1)
#        futures.append(exec.submit(bbpmpth, 0, digstart, digstart, digdisp,
#                                   0, 5))
#        pm.append(-1)
##        futures.append(exec.submit(bbpmpth, 0, digstart, digstart, digdisp,
##                                   0, 6))
#        print('start future #0-', len(futures))
#        rs = bbpmpth(0, digstart, digstart, digdisp, 0, 6)

        print('done future #', len(futures))
        rss = mpfr(8.) - rs
        for i in range(len(futures)):
            rss += pm[i] * futures[i].result()
            print('done future #', i)
        rss = gmpy2.frac(rss)
#    print('---')
    for k in range(digstart, digstart + overdig):
        rs = 16 ** (digstart - k) * (mpfr(4.) / (8 * k + 1) -\
                                     mpfr(2.) / (8 * k + 4) -\
                                     mpfr(1.) / (8 * k + 5) -\
                                     mpfr(1.) / (8 * k + 6))
        rss += rs
        rss = gmpy2.frac(rss)
#        print(k, ':', rss)
    return rss


def bbpmpth2(d0, d1, digstart, digdisp):
    fpprec = len(str(digstart)) + 4 * digdisp + 20
    gmpy2.get_context().precision = fpprec
    print(d0, ':', d1, '/', digstart, end = '->')
    rss = mpfr(0.)
    for k in range(d0, d1):
        k8 = k << 3
        dk = mpz(digstart - k)
        rs = mpfr(4.) + \
                 mpfr(gmpy2.powmod(mpz(16), dk, k8 + 1) << 2) / (k8 + 1) -\
                 mpfr(gmpy2.powmod(mpz(16), dk, k8 + 4) << 1) / (k8 + 4) -\
                 mpfr(gmpy2.powmod(mpz(16), dk, k8 + 5)     ) / (k8 + 5) -\
                 mpfr(gmpy2.powmod(mpz(16), dk, k8 + 6)     ) / (k8 + 6)
        rss += rs
        rss = gmpy2.frac(rss)
    print(rss)
    return rss


## divide process (into 8) by loop count
def bbpmpgmp2(digstart, digdisp):
    digstart = digstart - 1
    overdig = digdisp + 10
    rss = mpfr(0.)
    ndiv = 8
    futures = []
    with Executor() as exec:
        nd1 = 0
        for i in range(ndiv - 1):
            nd0, nd1 = nd1, int(digstart / ndiv * (i + 1))
            futures.append(exec.submit(bbpmpth2, nd0, nd1, digstart, digdisp))
        nd0, nd1 = nd1, digstart
        print('start future #0-', len(futures))
        rss = bbpmpth2(nd0, nd1, digstart, digdisp)
        for i in range(len(futures)):
            rss += futures[i].result()
            print('done future #', i)
        rss = gmpy2.frac(rss)
#    print('---')
    for k in range(digstart, digstart + overdig):
        rs = 16 ** (digstart - k) * (mpfr(4.) / (8 * k + 1) -\
                                     mpfr(2.) / (8 * k + 4) -\
                                     mpfr(1.) / (8 * k + 5) -\
                                     mpfr(1.) / (8 * k + 6))
        rss += rs
        rss = gmpy2.frac(rss)
#        print(k, ':', rss)
    return rss


def bellard(digstart):
    digstart = int((digstart - 3) / 5) * 2
    print('dig', digstart * 2.5 + 3, '... (digstart', digstart, ')')
    overdig = 6
    rss = 0.
    for k in range(0, digstart):
        rs = \
             - pow(1024, digstart - k, 4 * k + 1)  *  32 / (4 * k + 1)  \
             - pow(1024, digstart - k, 4 * k + 3)        / (4 * k + 3)  \
             + pow(1024, digstart - k, 10 * k + 1) * 256 / (10 * k + 1) \
             - pow(1024, digstart - k, 10 * k + 3) *  64 / (10 * k + 3) \
             - pow(1024, digstart - k, 10 * k + 5) *   4 / (10 * k + 5) \
             - pow(1024, digstart - k, 10 * k + 7) *   4 / (10 * k + 7) \
             + pow(1024, digstart - k, 10 * k + 9)       / (10 * k + 9)
        if k % 2 == 0:
            rss += rs
        else:
            rss -= rs
        rss, _ = math.modf(rss)
#        print(k, ':', rss)
#    print('---')
    for k in range(digstart, digstart + overdig):
        rs = (1024 ** (digstart - k)) * (
                      -32   / (4 * k + 1) \
                      -   1 / (4 * k + 3) \
                      + 256 / (10 * k + 1) \
                      -  64 / (10 * k + 3) \
                      -   4 / (10 * k + 5) \
                      -   4 / (10 * k + 7) \
                      +   1 / (10 * k + 9))
        if k % 2 == 0:
            rss += rs
        else:
            rss -= rs
#        rss = rss - int(rss)
        rss, _ = math.modf(rss)
#        print(k, ':', rss)
    rss, _ = math.modf(1. + rss)
    return rss


if __name__ == '__main__':
    global fpprec
    if len(sys.argv) != 2:
        print('usage: bbp DIGSTART', file = sys.stderr)
        sys.exit(1)
    digstart = int(sys.argv[1])
    digdisp = 16
# precision requires at least
# (displayed_precisions + loop_error + redundant)
    fpprec = len(str(digstart)) + 4 * digdisp + 20
    gmpy2.get_context().precision = fpprec
    print('prec:', gmpy2.get_context().precision)
#
## simple BBP
#    rss = bbp(digstart)
#    irss = int(rss * (16 ** 10))
#
## simple Bellard
#    rss = bellard(digstart)
#    irss = int(rss / 64 * (1024 ** 4))
# 2 + (startdig - 1) * 2.5 [digits]...
#
## single process, gmpy2
#    rss = bbpgmp(digstart, digdisp)
## divide process (into 8) by loop count
#    rss = bbpmpgmp2(digstart, digdisp)
## divide process (into 8) by term (into 4) & loop count (into 2)
    rss = bbpmpgmp(digstart, digdisp)
    irss = int(gmpy2.floor(rss * (16 ** (digdisp))))
##   int(gmfr) is rounded!!
##   bad: irss = int(rss * (16 ** (digdisp + 4)))
#
    print(hex(irss)[2:])
#    print(bin(irss)[2:])
