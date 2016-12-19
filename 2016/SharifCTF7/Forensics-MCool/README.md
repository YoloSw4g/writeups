# Sharif CTF 7 - MCool (250pts)

```
nc ctf.sharif.edu 4002
```

This challenge was all about MD5.
Basically, when you connect to the provided address, the server sends you a series of challenge.
This is an example output of the server banner and the first challenge:

```
----------------------------------------
Welcome to MD5Cool challenge server
----------------------------------------
In each stage send two distinct strings with desired property
Sent two different string separeted by new line with same md5 hash with len 163 and ends with MupxtCWBKFMEjEyGDFPW1EnSFZiKqxLWmKN
```

So the basic idea is to generate arbitrary collisions of a given length (between 100 and 300 bytes) ending with the given suffix.
However, the following constraints applies: the colliding strings must be separated by a specific separator, amongst:
 * single space
 * `=` sign
 * newline (0x0A) character

So the **strings you will be sending must not include these characters**, or the server will fail to parse your input.
Solving the rest of the challenge was easier, since (speaking of 64-byte blocks), the following applies:

```
Hypothesis:
M1 != M2
MD5(M1) = MD5(M2)

Then, whatever message M: MD5(M1 || M) = MD5(M2 || M)
```

You just have to find already existing collisions and complete with something, and then the suffix.
Since the total length can be as low as 90 and the suffix can take 25 characters, I had to search only collisions on 64-byte blocks.
Searching the Internet, I came accross multiple collisions example, but I had a hard time finding 64-byte colliding blocks without a space character (0x20) in it.
After a long hour of search, I came up with these ones:

```
Without '=' or newline:
0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef
0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef

Without ' ':
5D11693E1E334B2CB388EFAAF0D0ECF3912D730A1CDD7AAC6E3CE0E4CE067BB18E73C7BAA26AA81966C28616B34F3D07AAB7C81E329489647C11734A3FAF03EA
5D11693E1E334B2CB388EFAAF0D0ECF3912D730A1CDD7AAC6E3CE0E4CE067BB18E73C7BCA26AA81966C28616B34F3D07AAB7C81E329489E47C11734A3FAF03EA
```

The Python solution I wrote is at https://github.com/YoloSw4g/writeups/blob/master/2016/SharifCTF7/Forensics-MCool/forensics-mcool.py
And after many challenges, there goes the flag:

```
Great, you got flag
SharifCTF{aa4fc188fc86d11e25ecb220f7ce5e42}
```
