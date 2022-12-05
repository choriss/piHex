import gmpy2
import math
import sys


#limitblocks = -1
shift = 1000000000
#shift = 8

pklprefix = 'PATH_TO_piconv-'

def pkldump(var, fname):
    if isinstance(var, str):
        return var
    fn = pklprefix + fname + '.pkl'
    print('dump to {}'.format(fn), file = sys.stderr)
    with open(fn, 'wb') as fp:
        pickle.dump(var, fp)
    return fn


def pklload(var):
    if isinstance(var, str):
        fn = var
        print('load from {}'.format(fn), file = sys.stderr)
        with open(fn, 'rb') as fp:
            var = xmpz(pickle.load(fp))
    return var


if len(sys.argv) < 3 or 4 < len(sys.argv):
    print('piconvbin2.py INFILE.txt OUTFILE.bin [DIGITS]', file = sys.stderr)
    sys.exit(1)
if len(sys.argv) == 4:
    ndigs = int(sys.argv[3])
else:
    ndigs = -1
infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, 'r') as fp:
    s = fp.readline()
    s = fp.readline()
    s = fp.readline()
    if ndigs == -1:
        s = fp.readline()
    else:
        s = fp.read(ndigs + 1)
print('read', len(s), file = sys.stderr)

ia = int(s[0])
s = s[1:]
with open(outfile, 'wb') as fp:
    fp.write(ia.to_bytes(1, 'big'))
print('written int, trunc', file = sys.stderr)

a = gmpy2.xmpz(s)
if ndigs == -1:
    pkldump(a, 'pifixfrac')
    print('dumped', file = sys.stderr)
diga = gmpy2.num_digits(a)
bita = int(math.ceil(diga / math.log10(2)))
print('conv', diga, '(10-)digits, ', bita, '(2-)bits', file = sys.stderr)
del s
bytea = (bita + 7) // 8
nblks = (bytea + shift - 1) // shift
nfrac = bytea % shift
nbfrac = bita % 8
print(nblks, 'blks: frac', nfrac, 'bytes +', nbfrac, 'bits')
lastmask = (1 << nbfrac) - 1   # 0..01..<nbfrac>..1
lastmask <<= (8 - nbfrac)      # 1..<nbfrac>..10..0
print('lastbyte mask', hex(lastmask))

c = gmpy2.xmpz(10) ** gmpy2.mpz(gmpy2.num_digits(a))
print('c', gmpy2.num_digits(c), 'digs, a', gmpy2.num_digits(a), 'digs')

cnt = 1
nblock = gmpy2.xmpz(1) << (shift << 3)
print('const', file = sys.stderr)
with open(outfile, 'ab') as fp:
#    print('{:02x}.'.format(ia), end = '', file = sys.stderr)
#    while nblock < c:
    keepprec = diga
    for i in range(nblks):
# since (initial) c == 10 ** diga == (2 ** diga) * (5 ** diga),
# shifting c right less than or equals to diga bits
#   (c >> diga) [bits] doesn't lose precision
        if shift <= keepprec // 8:
            print('shift c>>', shift << 3, 'bits')
            c >>= (shift << 3)
            keepprec -= shift * 8
        else:
            a <<= (shift << 3)
            print('shift a<<', shift << 3, 'bits')
        print('a[', gmpy2.num_digits(a), ']//c[',
              gmpy2.num_digits(c), '] digs', file = sys.stderr)
        ah = int(a // c)
        if i < nblks - 1 or (i == nblks - 1 and nfrac == 0):
            fp.write(ah.to_bytes(shift, 'big'))
        else:
            print(shift, nfrac)
            ah >>= ((shift - nfrac) << 3)
            if nbfrac == 0:
                fp.write(ah.to_bytes(nfrac, 'big'))
            else:
                lastbyte = ah & lastmask
                ah >>= 8
                fp.write(ah.to_bytes(nfrac - 1, 'big'))
                fp.write(lastbyte.to_bytes(1, 'big'))
        a %= c
        cnt += 1
    print('c', gmpy2.num_digits(c), 'digs, a', gmpy2.num_digits(a), 'digs')

#print(file = sys.stderr)


