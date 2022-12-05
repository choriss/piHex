# https://www.mk-mode.com/blog/2015/05/06/cpp-pi-computation-by-chudnovsky-bsa-with-gmp/

import math
import sys
import time
import gmpy2
from gmpy2 import mpz
from gmpy2 import xmpz
from concurrent.futures import ProcessPoolExecutor as Executor
import pickle

# fork into (2 ^maxproclev) processes,
# thus maxproclev <- int(log2(# CPU core)) - 1
# 4 @<1e9 digits
maxproclev = 4
#maxproclev = -1

a = mpz(13591409)
b = mpz(545140134)
c = mpz(640320)
d = mpz(426880)
e = mpz(10005)
c3_24 = c * c * c // 24
errdig = 2
digits_per_term = math.log(53360 ** 3) / math.log(10)


def prettyprint(p):
#    ps = str(p)[:digits + 1]
    ps = str(p)
    dig = len(ps)
    print('pi = ', ps[0], '.', sep = '')
    for n in range(1, dig + 10, 10):
        print(ps[n:n + 10], end = '')
        if n % 50 == 41:
            print()
        else:
            print(' ', end = '')
    print()


def comppqt(n1, n2, lev):
    if n1 + 1 == n2:
        p = (2 * n2 - 1) * (6 * n2 - 1) * (6 * n2 - 5)
        q = c3_24 * n2 * n2 * n2
        t = (a + b * n2) * p
        if n2 % 2 == 1:
            t = -t
    else:
        m = (n1 + n2) // 2
        if lev <= maxproclev:
            with Executor() as exec:
#                future1 = exec.submit(comppqt, n1, m, lev + 1)
                future2 = exec.submit(comppqt, m, n2, lev + 1)
#                p1, q1, t1 = future1.result()
                p1, q1, t1 = comppqt(n1, m, lev + 1)
                p2, q2, t2 = future2.result()
                q = q1 * q2
                del q1
                p = p1 * p2
                del p2
                t = t1 * q2 + p1 * t2
        else:
            p1, q1, t1 = comppqt(n1, m, lev + 1)
            p2, q2, t2 = comppqt(m, n2, lev + 1)
            q = q1 * q2
            del q1
            p = p1 * p2
            del p2
            t = t1 * q2 + p1 * t2
    return p, q, t


def pi(digits):
    start = time.time()
    n = int(math.ceil((digits + errdig) / digits_per_term))
    prec = digits * math.log2(10)
    p, q, t = comppqt(mpz(0), mpz(n), 0)
    etime = time.time() - start

    print('elapsed time 1:', etime, '[sec]')
    print('elapsed time 1:', etime, '[sec]', file = sys.stderr)
    del p
    ntrunc = gmpy2.num_digits(t) - (digits + errdig)
    ntbase = mpz(10) ** mpz(ntrunc)
    t = t // ntbase
    q = q // ntbase
    del ntbase
    base2 = mpz(10) ** mpz(digits * 2)
    pi = d * gmpy2.isqrt(e * base2) * q
    del base2

    pi = pi // (a * q + t)

    etime = time.time() - start
    print('elapsed time 2:', etime, '[sec]')
    print('elapsed time 2:', etime, '[sec]', file = sys.stderr)
    print('pi({}):'.format(gmpy2.num_digits(pi) - 1))
    return pi


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage:', sys.argv[0], 'DIGITS')
        sys.exit(1)
    digits = int(sys.argv[1])
    p = pi(digits)

## gmpy2.mpz -> str is not affected by int_max_str_digits.
#if '3.11' <= sys.version:
#    sys.set_int_max_str_digits(digits + 10)
    print(p)
#    prettyprint(p)
#    print(file = sys.stderr)

