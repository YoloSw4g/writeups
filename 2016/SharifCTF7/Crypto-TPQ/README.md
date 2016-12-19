# Sharif CTF 7 - TPQ (150pts)

```
nc ctf.sharif.edu 4000
```

This challenge was about breaking RSA with knowing the modulus used.
When you connect to the server, the following banner is sent:

```
Our ultra-secure system is generating 10 primes... Done!
Please choose options quickly and carefully.
Options:
		[C]hoose two distinct indices to encrypt the flag
		[R]eveal the encryption function
		[Q]uit.
```

The encryption function was actually quite simple, since it's basic RSA:

```
def encrypt(m, p, q):
	e = 65537
	return gmpy2.powmod(bytes_to_long(m), e, p*q)
```

When choosing the first option, you have to select two indexes between 1 and 10, corresponding to one of the pre-generated primes.
You will receive the encrypted flag, however without knowing the used modulus:

```
Send two distinct indices smaller than 10, separated by space.
1 2
The encrypted flag is: 9046807966369013104443785094083357651804557086102562320476132401204946488424315424883736417174214338243583517673501651534568713405335693549656059449109489681445951414040911609199040282715702718701729417508560006185745957959421587581559806075271972117567441261775872539154858279105891072081173343765478887318
```

Ok, time to do some math, trying to exploit the fact that you can encrypt with moduli having a common prime.

```
First, notations:
- Primes are p[i], i=1..10
- Moduli are N[ij] = N[ji] = p[i]*p[j]
- Ciphertexts are C[ij] = RSA(flag, N[ij], e=0x10001)
- RSA formula is C = (M**e) % N

What if I take a common prime for two identical messages:

C[12] = M**e % N[12] => For some k[12]: C[12] = M**e + k[12]*p[1]*p[2]
C[13] = M**e % N[13] => For some k[13]: C[13] = M**e + k[13]*p[1]*p[3]

Therefore: C[13]-C[12] = p[1]*(k[13]*p[3]-k[12]*p[2])
Similarly: C[14]-C[12] = p[1]*(k[14]*p[4]-k[12]*p[2])

So p[1] divides every C[1i]-C[1j] for i,j in 1..10
```

Taking the GCD of every substraction has a high probability of giving back p[1]
If the GCD is prime, then we'll know for sure we have p[1], else we can try with another p[i].

Once we have two prime factors p[i] and p[j], we can reverse the RSA encryption:

```
n[ij] = p[i]*p[j]
phi = (p[i]-1)*(p[j]-1)
d = modinvert(e, phi)
flag = m**d % n[ij]
```

And finally, we have the flag:

```
Found prime GCD: 6985729662965991760744011089306603643903179054147637894434018803627594798613788357174046080923485027260146995548114994730469566535711077267591758519329969
Found prime GCD: 10153289248091314320765569663542656128058405162676128477330121760584994069087358322895378777001865604489340249791873858642903128127770349385216272339206841
N= 70928133877065165093244387701884275523033702387599514400909709325078307423749898854406400794407068031295776696386711660645494996198136903329856901424147936596088352452491116916462943663797512320827999959437700799785627874278653479569054279995844349123893713947713109391257075125057228676423681032324221117929
D= 37043626750449158045250299865115812176364459241691810411131689439229447586861033278737541944107376361066143472602108224675740463095195537286942368767959091615065884005590634174691603631536350107819952228020175629523158506070128135615622083394475232508525115881912367229282297077679263339706704335888325898753
Flag is: SharifCTF{7c62f12e7e6f08f9f5365e45588d34d8}
```

Python code available at https://github.com/YoloSw4g/writeups/blob/master/2016/SharifCTF7/Crypto-TPQ/crypto-tpq.py
For faster result, I didn't use all the 10 primes, just 6
