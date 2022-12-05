Some experimental Pi calculations using Python3 + gmpy2.

Scripts & BLOGs (in Japanese):

* pigl.py: Gauss--Legendre algorithm, basic Python int (fixed floating point)
* piglgm.py: Gauss--Legendre algorithm with gmpy2
https://zenn.dev/taroh/articles/c965946e457059 (got 4G decimal digits using Macbook Pro)

* pichgmmt.py: Chudnovsky algorithm, gmpy2, multi-thread
https://zenn.dev/taroh/articles/c0e984c13691ad (got 10G decimal digits using AWS)

* pibinconv2a.py: convert decimal text file -> binary file
https://zenn.dev/taroh/articles/38a8855a894fec (10G decimal digits text -> 4.15GB bin)

* bbp.py: BBP/Bellard algorithm, gmpy2, multi-thread
https://zenn.dev/taroh/articles/632f2ecf695e26 (verifyed 8.30G..+16 hex digits, tail of bin file above)
