#!/usr/bin/python

import utils

RULE = [86 >> i & 1 for i in range(8)]
NBYTES = 32
N = 8*NBYTES

def next(x):
    x = (x & 1) << N+1 | x << 1 | x >> N-1
    y = 0
    for i in range(N):
        y |= RULE[(x >> i) & 7] << i
    return y


c1 = open('rule86.txt', 'rb').read()
c2 = open('rule86.txt.enc', 'rb').read()
c3 = open('hint.gif.enc', 'rb').read()
c4 = open('hint.gif','wb')

k = utils.xor(c1,c2)[:NBYTES]
k = utils.from_bytes(k)
print k

for i in range(0, len(c3), 32):
    c4.write(utils.xor(utils.from_int(k),c3[i:i+32]))
    k = next(k)

c4.close()
