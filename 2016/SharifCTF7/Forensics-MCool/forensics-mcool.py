#!/usr/bin/python

import hashlib
import re
import socket

def recv(s, l=1024):

    d = s.recv(l)

    for l in d.replace('\r\n', '\n').split('\n'):
        print '<<< %s' % l

    return d


def send(s, d):

    for l in d.replace('\r\n', '\n').split('\n'):
        print '>>> %s' % l

    s.send(d)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ctf.sharif.edu', 4002))

d = recv(s)

def chall1():
    d = recv(s)

    t = d.split('\n')
    l = t[-2]
    p = r'^Sent two different string separeted by (.+) with same md5 hash with len (.+) and ends with (.+)$'
    m = re.match(p, l)

    sep = m.group(1)
    sep = sep[-1] if 'character' in sep else sep
    sep = ' ' if sep == 'single space' else sep
    sep = '\n' if sep == 'new line' else sep
    siz = int(m.group(2))
    end = m.group(3)

    print '<%s> <%d> <%s>' % (sep,siz,end)

    if sep!=' ':
        m1 = '0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef'.decode('hex')
        m2 = '0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef'.decode('hex')
    else:
        m1 = '5D11693E1E334B2CB388EFAAF0D0ECF3912D730A1CDD7AAC6E3CE0E4CE067BB18E73C7BAA26AA81966C28616B34F3D07AAB7C81E329489647C11734A3FAF03EA'.decode('hex')
        m2 = '5D11693E1E334B2CB388EFAAF0D0ECF3912D730A1CDD7AAC6E3CE0E4CE067BB18E73C7BCA26AA81966C28616B34F3D07AAB7C81E329489E47C11734A3FAF03EA'.decode('hex')

    assert((m1!=m2) and (hashlib.md5(m1).hexdigest()==hashlib.md5(m2).hexdigest()))

    szIns = siz - len(m1) - len(end)
    mm1 = m1 + 'a'*szIns + end
    mm2 = m2 + 'a'*szIns + end

    assert(hashlib.md5(mm1).hexdigest()==hashlib.md5(mm2).hexdigest())
    send(s, mm1+sep+mm2)

while(1):
    chall1()

recv(s)
