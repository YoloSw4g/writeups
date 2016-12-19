# Sharif CTF 7 - Playfake (50pts)

For this challenge we had a cipher text and the python script used to encode the passphrase `KPDPDGYJXNUSOIGOJDUSUQGFSHJUGIEAXJZUQVDKSCMQKXIR`.

Reading the script gives us some informations:  
- The passphrase is an english sentence;
- The passphrase contains the keywords `SharifCTF` and `contest`;
- The algorithmes used to encode the message.

Let's try to analyse the encoding function :
```
def playfair_enc(key, msg):
    assert len(msg) % 2 == 0
    assert len(key) == 25
    ctxt = ''
    for i in range(0, len(msg), 2):
        r0, c0 = get_pos(key, msg[i])
        r1, c1 = get_pos(key, msg[i+1])
        if r0 == r1:
            ctxt += get_letter(key, r0+1, c0+1) + get_letter(key, r1+1, c1+1)
        elif c0 == c1:
            ctxt += get_letter(key, r0-1, c0-1) + get_letter(key, r1-1, c1-1)
        else:
            ctxt += get_letter(key, r0+1, c1-1) + get_letter(key, r1+1, c0-1)
    return ctxt
```

So we write the decoding function:
```
def playfair_dec(key, ctxt):
    msg = ''
    for i in range(0, len(ctxt), 2):
        r0, c0 = get_pos(key, ctxt[i])
        r1, c1 = get_pos(key, ctxt[i+1])
        if r0 == r1:
            msg += get_letter(key, r0-1, c0-1) + get_letter(key, r1-1, c1-1)
        elif c0 == c1:
            msg += get_letter(key, r0+1, c0+1) + get_letter(key, r1+1, c1+1)
        else:
            msg += get_letter(key, r0-1, c1+1) + get_letter(key, r1-1, c0+1)
    return msg
```

But we don't know witch key was used but as we have seen, the initial key is just 5 cars length, we can brute-force using the cribble (we know to words of the final sentence):
```
if __name__ == '__main__':
    ctxt = "KPDPDGYJXNUSOIGOJDUSUQGFSHJUGIEAXJZUQVDKSCMQKXIR"
    for perm in itertools.permutations(ascii_uppercase, r=5):
        key = ''.join(perm) + ascii_uppercase
        key = make_key(key)
        msg = playfair_dec(key, ctxt)
        if re.search("SHARIFCTF", msg) and re.search("CONTEST", msg):
            print msg
```

We execute the script and after few seconds we got some answers:
```
m33d@hack:/tmp $ python medfair.py 
CURYRENTLYTHESEWENTHSHARIFCTFCONTESTKYPEINGHELDY
CURYRENTLYTHESEVENTHSHARIFCTFCONTESTISPEINGHELDY
```

Using the sentence `Currently the seventh SharifCTF contest is being held` we have the flag:
```
SharifCTF{655ad15484a60457f3af49512a5d5206}
```
