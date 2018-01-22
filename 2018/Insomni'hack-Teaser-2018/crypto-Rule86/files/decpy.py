#!/usr/bin/python

import utils

c1 = open('rule86.txt', 'rb').read()
c2 = open('rule86.txt.enc', 'rb').read()
c3 = open('super_cipher.py.enc', 'rb').read()
c4 = open('super_cipher.py','wb')

s = utils.xor(c1,c2)
c4.write(utils.xor(c3, s))
