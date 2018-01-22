#!/usr/bin/python

import utils
import os
import sys

RULE = [86 >> i & 1 for i in range(8)]
IRULE = {'0':[], '1':[]}

for bit in [0,1]:
    for i in range(len(RULE)):
        if RULE[i]==bit:
            IRULE[str(bit)].append(bin(i)[2:].zfill(3)[::-1])


NBYTES = 32
N = 8*NBYTES

# 32 to 34 bits
def next1(x):
    return (x & 1) << N+1 | x << 1 | x >> N-1

def invnext1(y):
    x = (y>>1)&0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    return x

def next2(x):
    y = 0
    for i in range(N):
       y |= RULE[(x >> i) & 7] << i
    return y


def invnext2(x):
    binin = bin(x)[2:].zfill(N)[::-1]
    valid = ['']
    for i in range(0, len(binin)):

        bit=binin[i]

        newvalid = []
        for v in valid:
            for group in IRULE[bit]:
                if i>0 and v[-2:]==group[:2]:
                    newvalid.append(v[:-2]+group)
                elif i==0:
                    newvalid.append(group)

        valid = newvalid

    binin = None
    for v in valid:
        if v[:2] == v[-2:]:
            binin = int(v[::-1], 2)

    if binin is None:
        print 'Error !'
        sys.exit(1)

    return binin


def next(x):
    return next2(next1(x))


# First keystream block from rule86.txt encryption
m1 = utils.from_bytes('e29375b5fb90f170d6b88c98c0d5bfba15c04d9023915b8fc2f2e324c12ccc52'.decode('hex'))
y=m1


for c in range(N//2):

    step = invnext2(y)
    x = invnext1(step)
    y = x

print utils.from_int(y)
