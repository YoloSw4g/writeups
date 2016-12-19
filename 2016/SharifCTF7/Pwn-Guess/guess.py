#!/usr/bin/python
s = ""
with open("output.txt","r") as f:
    s = f.read()

s = s.strip()
s = s.split("-")
s_int = map(int, s)
s_hex = map(hex, s_int)

s_hex16 = map( lambda x : x[2:].zfill(16) if not 'L' in x else x[2:-1].zfill(16), s_hex)

s_string = map(lambda x : x.decode('hex')[::-1], s_hex16)
#print s_string

print "".join(s_string)
