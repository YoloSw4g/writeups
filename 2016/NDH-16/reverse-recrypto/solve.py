#!/usr/bin/env python
import string

## SBOX

SBOX_1 = [
    0x09,0x43,0xbb,0x88,0xda,0x23,0xf1,0x5f,0xad,0x8d,0x7e,
    0x02,0xba,0xe1,0x0f,0x6c,0x21,0x55,0xf2,0xb2,0xd1,0xa6,
    0x30,0x14,0x3b,0x26,0x24,0xde,0x91,0xc3,0xe8,0x52,0xcc,
    0x49,0xa1,0xa8,0xc6,0xed,0x39,0x86,0xb7,0xb8,0x68,0xd7,
    0xf0,0x03,0x9e,0xe9,0x80,0x15,0x8c,0x4d,0xe5,0xe6,0xdc,
    0xf4,0x29,0x0d,0x2c,0x04,0x1d,0xac,0x41,0x56,0xb6,0x19,
    0x72,0xfd,0x77,0x16,0x2e,0x73,0xca,0x46,0xaf,0x58,0x3c,
    0xd0,0xb9,0x79,0xd6,0xbd,0xe7,0x5e,0x6d,0x64,0x2b,0x74,
    0x32,0x50,0x75,0xd2,0x28,0x0a,0x01,0x1f,0x8e,0x82,0x40,
    0x31,0xf8,0x85,0xc0,0x37,0xa7,0x4f,0xd3,0xa4,0x96,0xa2,
    0x0c,0x11,0x78,0x45,0xf7,0xee,0x89,0xcd,0x7b,0x3d,0x1a,
    0x9b,0x0e,0xf9,0x06,0x59,0x90,0xe3,0xdb,0x4b,0x00,0x38,
    0x9c,0x71,0x4c,0x20,0x9a,0xcb,0xe4,0xb4,0xa3,0xbc,0x65,
    0xc5,0x1b,0x8b,0x2d,0x81,0xe0,0x8a,0x34,0x87,0x5b,0xbe,
    0x44,0x92,0x93,0x99,0x7d,0xf6,0xc4,0xe2,0x0b,0xaa,0xa0,
    0x12,0x62,0xb5,0x9d,0x08,0x76,0x61,0xf5,0xeb,0x33,0x2a,
    0xae,0x97,0x3e,0xbf,0x35,0x36,0xd8,0x10,0xf3,0xc8,0xdf,
    0x6b,0x25,0xc1,0x42,0x05,0xd9,0xea,0xb1,0xd5,0x6e,0x60,
    0xd4,0xa5,0x7f,0x63,0x4a,0xc7,0xec,0xb0,0xfe,0x4e,0x8f,
    0x94,0xef,0xfc,0x17,0x6f,0xb3,0x98,0xdd,0x1e,0x27,0x54,
    0x5a,0x9f,0x69,0x84,0x5d,0x67,0x13,0xab,0xa9,0x18,0x3f,
    0xcf,0xc9,0x51,0x66,0xc2,0x2f,0x7a,0xff,0x6a,0x53,0x95,
    0x83,0x48,0xce,0x7c,0x47,0x70,0x57,0x3a,0xfa,0xfb,0x07,
    0x22,0x5c,0x1c]

SBOX_2 = [
    0x99,0xfb,0x7b,0xc1,0x9d,0x40,0xf3,0x0f,0x26,0xce,0x91,
    0x56,0xad,0x70,0x74,0x79,0x35,0x33,0x89,0x0e,0x39,0x6f,
    0x66,0x3b,0xba,0xae,0xc4,0x83,0x55,0xb8,0x08,0x9e,0xb9,
    0x25,0x47,0xaa,0x45,0x2d,0xe2,0x34,0x81,0x48,0xd5,0x12,
    0x51,0x0c,0x9a,0x8e,0x30,0x5d,0x6a,0xfd,0x1b,0x4b,0xd0,
    0x1a,0x96,0x82,0xff,0xeb,0x4f,0x0a,0x5f,0x4c,0x23,0xef,
    0x50,0x3c,0x80,0x95,0x60,0xd4,0x15,0xf4,0x11,0x62,0xa5,
    0xb5,0xbd,0x78,0x3e,0x6e,0xa6,0x61,0xb3,0x75,0xf5,0x85,
    0xd7,0xc9,0xf0,0x28,0xd9,0x00,0xb2,0x90,0x2f,0xc3,0x71,
    0xd8,0xcb,0x86,0x4a,0x3f,0x88,0xe8,0x46,0x73,0x87,0xe7,
    0x07,0x2c,0xb1,0x36,0x04,0x43,0x7c,0x1c,0xbe,0xc2,0x69,
    0xd2,0xed,0xf2,0xbc,0xb4,0xaf,0xf8,0xe4,0x5e,0x63,0x17,
    0x31,0xe5,0xc8,0xb7,0x2e,0x2b,0xc5,0xab,0x22,0x97,0xcd,
    0x5c,0xcf,0xc6,0xf1,0x98,0xe9,0xd3,0xa1,0x8c,0x44,0x9b,
    0xc7,0x2a,0xf7,0x1f,0xbf,0xd1,0x76,0x94,0x77,0xdf,0xb0,
    0xa2,0x8d,0x7e,0x29,0x5a,0xbb,0xa0,0xdb,0x13,0x64,0xa3,
    0x32,0x4e,0x01,0x8f,0x03,0xf9,0x20,0x7f,0x27,0xa8,0x24,
    0x09,0xec,0x3a,0x0b,0x02,0x3d,0xc0,0x06,0xa7,0x0d,0x6c,
    0x38,0x37,0x72,0x57,0xa9,0x6d,0xd6,0x93,0xfe,0xdd,0x8b,
    0xcc,0x65,0x6b,0xca,0xea,0xde,0x18,0x8a,0x9c,0xdc,0x16,
    0xb6,0xe0,0x14,0x52,0x4d,0x92,0xe6,0x54,0x05,0xfc,0x19,
    0x84,0x10,0x42,0x9f,0xac,0x1d,0x53,0xda,0x68,0x67,0x41,
    0x58,0x5b,0xa4,0x7d,0x7a,0x21,0x59,0xe1,0xf6,0xe3,0xfa,
    0x1e,0xee,0x49]

## Utils

def get_qword(t, i):
    res = 0
    for j in range(7, -1, -1):
        res <<= 8
        res |= t[i+j]
    return res


def set_qword(t, i, val):
    for j in range(8):
        t[i+j] = val & 0xFF
        val >>= 8


def rol_64(val, n):
    return ((val << n) | (val >> (0x40 -n))) & (2**0x40 - 1)


def ror_64(val, n):
    return ((val >> n) | (val << (0x40 -n))) & (2**0x40 - 1)


def get_content(filename):
    with open(filename, "rb") as f:
        return f.read()


def invert_permutation(P):
    P_inv = [0] * len(P)

    for i in range(len(P)):
        P_inv[P[i]] = i

    return P_inv


def rotate_matrix(matrix, i):

    for _ in range(i):
        matrix = matrix[0x10:] + matrix[0:0x10]

    return matrix

## Crypto functions

def generate_keystream(key):
    global SBOX_1

    K   = map(ord, list(key))
    l   = len(key) - 1
    res = [0] * 0x100
    P   = [SBOX_1[i] for i in range(0x100)]
    v   = 0

    while l >= 0:
        
        for i in range(0x100):
            res[i] = P[P[i] ^ K[l]]

        P = [res[i] for i in range(0x100)]
        v = get_qword(P, 0)
        l -= 1

    return v


def next_derived(val):
    val &= 0xFFFFFFFF
    return ror_64(val ^ rol_64(val, 3), 2)


def shuffle_buffer(buf, offset, key):

    for i in range(0xF):
        a = (key & (0x0F << i)) >> i
        b = (key & (0xF0 << i)) >> (i+4)

        buf[offset+a], buf[offset+b] = buf[offset+b], buf[offset+a]

    return buf


def pseudo_encrypt(buf, offset, key):
    global SBOX_2

    # Rotate the SBOX_2
    SBOX_2 = SBOX_2[0x10:] + SBOX_2[0:0x10]


    # XOR the SBOX_2
    for i in range(0x100):
        SBOX_2[i] = (SBOX_2[i] ^ key) & 0xFF

    # XOR the buffer
    for i in range(0x10):
        buf[offset+i] = buf[offset+i] ^ SBOX_2[i]

    res = shuffle_buffer(buf, offset, key)

    return res


def encrypt(key, clear):
    size = len(clear)
    C    = 0xA247A1E304738C7B

    if size % 0x10 == 0:
        res = map(ord, list(clear))
    else:
        res = map(ord, list(clear)) +  [0] * (0x10 - (size % 0x10))

    for i in range(0, size, 0x10):

        res = pseudo_encrypt(res, i, key)

        p1, p2 = get_qword(res, i), get_qword(res, i+8)
        new_C = p1 ^ p2

        print "Encrypted before last XOR"
        print res[i:i+0x10]

        set_qword(res, i  , p1 ^ C)
        set_qword(res, i+8, p2 ^ C)

        C = new_C

        key = next_derived(key)

    return res


def encrypt_file(key, i_file, o_file):
    content = get_content(i_file)

    d_value = generate_keystream(key)
    cipher = encrypt(d_value, content)

    with open(o_file, "wb") as f:
        f.write("".join(map(chr, cipher)))

## Solve functions

def brute_perm(orig):
    orig = set(orig)
    global SBOX_2

    for i in range(0x1):
        f = lambda x: x ^ ord('a')
        M = map(f, SBOX_2)
        print M[0x10:0x20]

        for j in range(0, 0x100, 0x10):
            if orig.issubset(set(M[j:j+0x10])):
                print "Found potential vector !!!"


def get_all_blocks(filename):
    blocks  = []
    content = map(ord, get_content(filename))

    for i in range(0, len(content), 0x10):
        blocks.append(content[i:i+0x10])

    return blocks


def pseudo_decrypt(blocks):
    C    = 0xA247A1E304738C7B
    res  = []

    for block in blocks:
        p1, p2 = get_qword(block, 0), get_qword(block, 8)
        new_C = p1 ^ p2

        set_qword(block, 0, p1 ^ C)
        set_qword(block, 8, p2 ^ C)

        C = new_C

        res.append(block)

    return res


def solve():
    blocks = get_all_blocks("./to_decrypt.txt")
    blocks = pseudo_decrypt(blocks)

    l = len(blocks)

    kk = -1

    for k in range(0, l):

        # Copy of SBOX_2 then rotate
        perm = [SBOX_2[i] for i in range(0x100)]
        perm = rotate_matrix(perm, k+1)

        
        for i in range(0x100):
            p = map(lambda x: x ^ i, perm)
            p_inv = invert_permutation(p)

            s =  map(chr, map(lambda x, y: x ^ y, p[:0x10], blocks[k]))

            if all(map(lambda x: x in string.printable, s)):
                if "flag" in "".join(s).lower():
                    kk = i
                    break

        if kk != -1:
            break

    final = ""

    for k in range(38, l):

        # Copy of SBOX_2 then rotate
        perm = [SBOX_2[i] for i in range(0x100)]
        perm = rotate_matrix(perm, k+1)

        p = map(lambda x: x ^ kk, perm)
        p_inv = invert_permutation(p)

        s =  map(chr, map(lambda x, y: x ^ y, p[:0x10], blocks[k]))
        
        final += "".join(s)

    print final


if __name__ == "__main__":
    solve()
    flag = "ndh16_exatrackgiveyoumorepoints"
