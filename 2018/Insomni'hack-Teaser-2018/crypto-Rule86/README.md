# Crypto - Rule86

```
Kevin is working on a new synchronous stream cipher, but he has been re-using his key.
```

In this challenge, you are provided with 4 files:
* An [encrypted GIF](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/resources/hint.gif.enc)
* An [encrypted python script](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/resources/super_cipher.py.enc)
* A [cleartext file](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/resources/rule86.txt)
* The [encrypted version of said file](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/resources/rule86.txt.enc)

The goal appears to be quite clear: decrypt the GIF to find the flag.
I've put some utils functions in a [Python file](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/files/utils.py) to be used for the rest of the chall.

## Step 1/2: read the Python source
Rule86 is announced to be a stream cipher, so the keystream is derived from an original key and xored with the text.
We can retrieve the keystream used to encrypt `rule86.txt` by XOR-ing the file with `rule86.txt.enc`.
This can be found here, and gives the following result for `super_cipher.py` (truncated since `rule86.txt` keystream is shorter than `super_cipher.py`):

```python
#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("key")
args = parser.parse_args()

RULE = [86 >> i & 1 for i in range(8)]
N_BYTES = 32
N = 8 * N_BYTES

def next(x):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= RULE[(x >> i) & 7] << i
  return y

# Bootstrap the PNRG
keystream = int.from_bytes(args.key.encode(),'little')
for i in range(N//2):
  keystream = next(keystream)

# Encrypt / decrypt stdin to stdout
plainte
```

# Step 2/2: decrypt the GIF
Let's analyse a bit the encryption script.
A function next is used to generate a 32-byte integer from a 32-byte integer. The function next is applied 128 times to the Initialization Vector, and then used a stream cipher.
Since we know the key has been reused, we know that the keystream will be identical for the encryption of `rule86.txt` and `hint.gif`.
We can retrieve the first value of the keystream, and derive the rest since we have the `next` function.
Actually, the provided script is in Python 3, which I don't like, so I wrote the equivalent of `from_bytes` (and its counterpart `from_int` in [utils.py](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/files/utils.py)

The script used to decipher `hint.gif.enc` can be found [here](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/files/decgif.py)