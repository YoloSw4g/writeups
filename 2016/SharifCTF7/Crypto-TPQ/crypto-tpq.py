#!/usr/bin/python

import socket
from gmpy2 import mpz, gcd, invert, powmod, is_prime
import time

def recv(s, l=1024):

    d = s.recv(l)

    for l in d.replace('\r\n', '\n').split('\n'):
        print '<<< %s' % l
    return d


def send(s, d):

    for l in d.replace('\r\n', '\n').split('\n'):
        print '>>> %s' % l
    s.send(d)


def getencryption(s, i, j):

    recv(s) #menu
    send(s, "C")
    recv(s)
    send(s, "%d %d\n" % (i,j))

    resp = recv(s)
    return int(resp.split()[-1])


def getenc(enc, i, j):

    return enc[min(i,j)][max(i,j)]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ctf.sharif.edu', 4000))

recv(s, 57) #banner
time.sleep(1)

encryptions = {}

r = range(0,5) # faster than (0,10), gives approximatively good results
for i in r:

    encryptions[i] = {}
    for j in r:
        if i>=j:
            continue

        encryptions[i][j] = getencryption(s, i, j)

subs = {} # subs[i] = {C[ij]-C[ik]}
for i in r:
    subs[i] = []
    for j in r:

        if j==i:
            continue

        for k in r:

            if j>=k or i==k:
                continue

            subs[i].append( getenc(encryptions, i,j) - getenc(encryptions, i, k))

found_primes = []
for i in r:

    assert(len(subs[i])>=2)
    g = gcd( mpz(subs[i][0]), mpz(subs[i][1]))

    for j in range(2, len(subs[i])):
        g = gcd( g, mpz(subs[i][j]))

    if is_prime(g):
        print 'Found prime GCD: %d' % g
        found_primes.append((i, g))

    if len(found_primes)==2:
        break


assert(len(found_primes)==2)
p = found_primes[0][1]
q = found_primes[1][1]
n = p*q
print 'N= %d' %n

e = mpz(65537)
phi = (p-1)*(q-1)
d = invert(e, phi)
print 'D= %d' %d

m = powmod( getenc(encryptions, found_primes[0][0], found_primes[1][0]), d, n)

print 'Flag is: %s ' % hex(int(m))[2:-1].decode('hex')
