#!/usr/bin/python


import base64

f = open('unlucky.txt','rb')
co = f.read()
f.close()

c=0
m=''
s=''
for l in co.split('\n'):

    if c==2:
        open(m.encode('hex')+'.sig', 'wb').write(base64.b64decode(s))
        open(m.encode('hex'), 'w').write(m)
        c=0
        continue

    if c==1:
        s=l
        c=2
        continue

    if c==0:
        m=l
        c=1
        continue

