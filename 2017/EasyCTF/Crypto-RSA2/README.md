# EasyCTF - RSA 2

In this challenge, we are asked to decipher an RSA encoded message.
We are given N, e and C.

N looks quite small, so there is a chance it has already been factored online.
Using https://factordb.com, we find that `N = 338779901332693957541 * 381858611614052422763`.

There goes the rest of the challenge:

```python
#!/usr/bin/python

import gmpy2

p = 338779901332693957541
q = 381858611614052422763
e = 0x10001
c = 41786000149048295568588665335025364614298

phi = (p-1)*(q-1)
d = gmpy2.invert(e, phi)
m = pow(c, d, p*q)

print hex(m)[2:].replace('L','').decode('hex')
```

The result is `flag{l0w_n_0868}`.
