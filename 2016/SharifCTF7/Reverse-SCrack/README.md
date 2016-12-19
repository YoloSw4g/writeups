# Reverse - SCrack



```
[0x00400960]> pd 100 @ 0x0000000000400ad0
|           0x00400ad0      0fb645b0       movzx eax, byte [rbp - local_50h]
|           0x00400ad4      3c38           cmp al, 0x38                ; '8' ; '8'
|       ,=< 0x00400ad6      0f85bc030000   jne 0x400e98
|       |   0x00400adc      0fb645b1       movzx eax, byte [rbp - local_4fh]
|       |   0x00400ae0      3c37           cmp al, 0x37                ; '7' ; '7'
|      ,==< 0x00400ae2      0f85b0030000   jne 0x400e98
|      ||   0x00400ae8      0fb645b2       movzx eax, byte [rbp - local_4eh]
|      ||   0x00400aec      3c34           cmp al, 0x34                ; '4' ; '4'
|     ,===< 0x00400aee      0f85a4030000   jne 0x400e98
|     |||   0x00400af4      0fb645b3       movzx eax, byte [rbp - local_4dh]
|     |||   0x00400af8      3c30           cmp al, 0x30                ; '0' ; '0'
|    ,====< 0x00400afa      0f8598030000   jne 0x400e98
|    ||||   0x00400b00      0fb645b4       movzx eax, byte [rbp - local_4ch]
|    ||||   0x00400b04      3c33           cmp al, 0x33                ; '3' ; '3'
|   ,=====< 0x00400b06      0f858c030000   jne 0x400e98
|   |||||   0x00400b0c      0fb645b5       movzx eax, byte [rbp - local_4bh]
|   |||||   0x00400b10      3c38           cmp al, 0x38                ; '8' ; '8'
|  ,======< 0x00400b12      0f8580030000   jne 0x400e98
|  ||||||   0x00400b18      0fb645b6       movzx eax, byte [rbp - local_4ah]
|  ||||||   0x00400b1c      3c65           cmp al, 0x65                ; 'e' ; 'e'
| ,=======< 0x00400b1e      0f8574030000   jne 0x400e98
| |||||||   0x00400b24      0fb645b7       movzx eax, byte [rbp - local_49h]
| |||||||   0x00400b28      3c34           cmp al, 0x34                ; '4' ; '4'
| ========< 0x00400b2a      0f8568030000   jne 0x400e98
| |||||||   0x00400b30      0fb645b8       movzx eax, byte [rbp - local_48h]
| |||||||   0x00400b34      3c62           cmp al, 0x62                ; 'b' ; 'b'
| ========< 0x00400b36      0f855c030000   jne 0x400e98
| |||||||   0x00400b3c      0fb645b9       movzx eax, byte [rbp - local_47h]
| |||||||   0x00400b40      3c36           cmp al, 0x36                ; '6' ; '6'
| ========< 0x00400b42      0f8550030000   jne 0x400e98
| |||||||   0x00400b48      0fb645ba       movzx eax, byte [rbp - local_46h]
| |||||||   0x00400b4c      3c65           cmp al, 0x65                ; 'e' ; 'e'
| ========< 0x00400b4e      0f8544030000   jne 0x400e98
| |||||||   0x00400b54      0fb645bb       movzx eax, byte [rbp - local_45h]
| |||||||   0x00400b58      3c32           cmp al, 0x32                ; '2' ; '2'
| ========< 0x00400b5a      0f8538030000   jne 0x400e98
| |||||||   0x00400b60      0fb645bc       movzx eax, byte [rbp - local_44h]
| |||||||   0x00400b64      3c39           cmp al, 0x39                ; '9' ; '9'
| ========< 0x00400b66      0f852c030000   jne 0x400e98
| |||||||   0x00400b6c      0fb645bd       movzx eax, byte [rbp - local_43h]
| |||||||   0x00400b70      3c62           cmp al, 0x62                ; 'b' ; 'b'
| ========< 0x00400b72      0f8520030000   jne 0x400e98
| |||||||   0x00400b78      0fb645be       movzx eax, byte [rbp - local_42h]
| |||||||   0x00400b7c      3c66           cmp al, 0x66                ; 'f' ; 'f'
| ========< 0x00400b7e      0f8514030000   jne 0x400e98
| |||||||   0x00400b84      0fb645bf       movzx eax, byte [rbp - local_41h]
| |||||||   0x00400b88      3c30           cmp al, 0x30                ; '0' ; '0'
| ========< 0x00400b8a      0f8508030000   jne 0x400e98
| |||||||   0x00400b90      0fb645c0       movzx eax, byte [rbp - local_40h]
| |||||||   0x00400b94      3c38           cmp al, 0x38                ; '8' ; '8'
| ========< 0x00400b96      0f85fc020000   jne 0x400e98
| |||||||   0x00400b9c      0fb645c1       movzx eax, byte [rbp - local_3fh]
| |||||||   0x00400ba0      3c39           cmp al, 0x39                ; '9' ; '9'
| ========< 0x00400ba2      0f85f0020000   jne 0x400e98
| |||||||   0x00400ba8      0fb645c2       movzx eax, byte [rbp - local_3eh]
| |||||||   0x00400bac      3c38           cmp al, 0x38                ; '8' ; '8'
| ========< 0x00400bae      0f85e4020000   jne 0x400e98
| |||||||   0x00400bb4      0fb645c3       movzx eax, byte [rbp - local_3dh]
| |||||||   0x00400bb8      3c62           cmp al, 0x62                ; 'b' ; 'b'
| ========< 0x00400bba      0f85d8020000   jne 0x400e98
| |||||||   0x00400bc0      0fb645c4       movzx eax, byte [rbp - local_3ch]
| |||||||   0x00400bc4      3c67           cmp al, 0x67                ; 'g' ; 'g'
| ========< 0x00400bc6      0f85cc020000   jne 0x400e98
| |||||||   0x00400bcc      0fb645c5       movzx eax, byte [rbp - local_3bh]
| |||||||   0x00400bd0      3c34           cmp al, 0x34                ; '4' ; '4'
| ========< 0x00400bd2      0f85c0020000   jne 0x400e98
| |||||||   0x00400bd8      0fb645c6       movzx eax, byte [rbp - local_3ah]
| |||||||   0x00400bdc      3c66           cmp al, 0x66                ; 'f' ; 'f'
| ========< 0x00400bde      0f85b4020000   jne 0x400e98
| |||||||   0x00400be4      0fb645c7       movzx eax, byte [rbp - local_39h]
| |||||||   0x00400be8      3c30           cmp al, 0x30                ; '0' ; '0'
| ========< 0x00400bea      0f85a8020000   jne 0x400e98
| |||||||   0x00400bf0      0fb645c8       movzx eax, byte [rbp - local_38h]
| |||||||   0x00400bf4      3c32           cmp al, 0x32                ; '2' ; '2'
| ========< 0x00400bf6      0f859c020000   jne 0x400e98
| |||||||   0x00400bfc      0fb645c9       movzx eax, byte [rbp - local_37h]
| |||||||   0x00400c00      3c32           cmp al, 0x32                ; '2' ; '2'
| ========< 0x00400c02      0f8590020000   jne 0x400e98
| |||||||   0x00400c08      0fb645ca       movzx eax, byte [rbp - local_36h]
| |||||||   0x00400c0c      3c35           cmp al, 0x35                ; '5' ; '5'
| ========< 0x00400c0e      0f8584020000   jne 0x400e98
| |||||||   0x00400c14      0fb645cb       movzx eax, byte [rbp - local_35h]
| |||||||   0x00400c18      3c39           cmp al, 0x39                ; '9' ; '9'
| ========< 0x00400c1a      0f8578020000   jne 0x400e98
| |||||||   0x00400c20      0fb645cc       movzx eax, byte [rbp - local_34h]
| |||||||   0x00400c24      3c33           cmp al, 0x33                ; '3' ; '3'
| ========< 0x00400c26      0f856c020000   jne 0x400e98
| |||||||   0x00400c2c      0fb645cd       movzx eax, byte [rbp - local_33h]
| |||||||   0x00400c30      3c35           cmp al, 0x35                ; '5' ; '5'
| ========< 0x00400c32      0f8560020000   jne 0x400e98
| |||||||   0x00400c38      0fb645ce       movzx eax, byte [rbp - local_32h]
| |||||||   0x00400c3c      3c63           cmp al, 0x63                ; 'c' ; 'c'
| ========< 0x00400c3e      0f8554020000   jne 0x400e98
| |||||||   0x00400c44      0fb645cf       movzx eax, byte [rbp - local_31h]
| |||||||   0x00400c48      3c30           cmp al, 0x30                ; '0' ; '0'
| ========< 0x00400c4a      0f8548020000   jne 0x400e98
| |||||||   0x00400c50      be53000000     mov esi, 0x53               ; 'S'
| |||||||   0x00400c55      bfc0216000     mov edi, obj.std::cout      ; ".got.plt" @ 0x6021c0
| |||||||   0x00400c5a      e881fcffff     call fcn.004008e0
| |||||||   0x00400c5f      be68000000     mov esi, 0x68               ; 'h'
```

So we concanate all these cars to have the passphrase `874038e4b6e29bf0898bg4f0225935c0s`, we finally we got the flag:
```
m33d@hack:/tmp$ ./SCrack
Enter the valid key!
874038e4b6e29bf0898bg4f0225935c0s
SharifCTF{ed97d286f356dadb5cde0902006c7deb}
```

