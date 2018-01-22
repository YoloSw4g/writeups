#!/usr/bin/python

def xor(a,b):

    s=''
    for i,j in zip(a,b):
        s+=chr(ord(i)^ord(j))

    return s


def from_bytes(s):
    return int(s[::-1].encode('hex'), 16)

def from_int(i):
    return hex(i)[2:].replace('L','').zfill(64).decode('hex')[::-1]
