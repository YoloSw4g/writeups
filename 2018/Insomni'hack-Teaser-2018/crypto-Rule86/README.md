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
I've put some utils functions in a [Python script](https://github.com/YoloSw4g/writeups/blob/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/files/utils.py) to be used for the rest of the chall.

## Step 1/2: read the Python source
Rule86 is announced to be a stream cipher, so the keystream is derived from an original key and xored with the text.
We can retrieve the keystream used to encrypt `rule86.txt` by XOR-ing the file with `rule86.txt.enc`.
This can be found [here](https://github.com/YoloSw4g/writeups/blob/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/files/decpy.py), and gives the following result for `super_cipher.py` (truncated since `rule86.txt` keystream is shorter than `super_cipher.py`):

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

## Step 2/2: decrypt the GIF
Let's analyse a bit the encryption script.
A function next is used to generate a 32-byte integer from a 32-byte integer. The function next is applied 128 times to the Initialization Vector, and then used a stream cipher.
Since we know the key has been reused, we know that the keystream will be identical for the encryption of `rule86.txt` and `hint.gif`.
We can retrieve the first value of the keystream, and derive the rest since we have the `next` function.
Actually, the provided script is in Python 3, which I don't like, so I wrote the equivalent of `from_bytes` (and its counterpart `from_int` in [utils.py](https://github.com/YoloSw4g/writeups/blob/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/files/utils.py)).

The script used to decipher `hint.gif.enc` can be found [here](https://github.com/YoloSw4g/writeups/blob/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/files/decgif.py).
The deciphered GIF is:

![GIF](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/resources/hint.gif)

## Step 3/3: finding the flag
Ok, at this point, I really tried to avoid reversing the function `next`, but it know appears unavoidable.
The function is composed of two separate parts:
* First one takes the input on 256 bits, and extends it to 258 bits by shifting some
* Second one build the 256-bit output by relying on groups of 3 bits from the intermediate output and the 86 Rule, which is an array of the bits of 86


### Step 3.1: bit shift
Let's take a look at what performs the first one. For the sake of simplicity, we use a number with far less than 256 bits, and try to see what it becomes. Each letter, such as `a` or `b` represents a bit:

| Operation     | Result         |
| ------------- |----------------|
| `x`           | `00abcdefghij` |
| `(x&1)<<N+1`  | `j00000000000` |
| `x<<1`        | `0abcdefghij0` |
| `x>>N-1`      | `00000000000a` |
| **Result**    | `jabcdefghija` |

Reversing that is easy, we only have to perform `x = (y>>1) & 0xffffffffffffffffffffffffffffffff`.

### Step 3.2: rule masking
This one is a little trickier. The algorithme takes the rightmost group of three bits, which forms a number between 0 and 7, and takes the correspoding bit value in the `RULE` array and sets this bit a the LSB in the final result.
Then it moves to the next group of three bits (overlapping on two bits with the previous one) and repeats the process to compute the second LSB bit. Etc.

if we want to reverse this step, we have to take into account multiple things:
* 86 is balanced, its binary representation has as many 1s as 0s
* The pre-image of a single bit can be 4 values
* Knowing that the pre-images of two consecutive bits overlap on two bits, we have a first condition to reduce the possible number of values
* The result of the first step has a final condition which is that the two leftmost bits are identical to the two rightmost bits, which drops the number of possible solutions to 1

A [really dirty Python script](https://github.com/YoloSw4g/writeups/blob/master/2018/Insomni%27hack-Teaser-2018/crypto-Rule86/files/revnext.py) takes all that into account to reverse the 128 first iterations of next, and retrieve the flag:
```
$ python revnext.py
INS{Rule86_is_W0lfr4m_Cha0s}
```