![img](../../../../../assets/htb.png)

<img src='../../../../../assets/logo.png' style='zoom: 80%;' align=left /><font size='5'>binary basis</font>

​	30<sup>th</sup> September 2024 / Document No. D24.102.XX

​	Prepared By: `rasti`

​	Challenge Author(s): `rasti`

​	Difficulty: <font color=green>Easy</font>

​	Classification: Official

# Synopsis

- `binary basis` is an easy challenge. The player has to examine the provided hint value which is a linear combination of 16 RSA primes with the coefficients being continuously decreasing powers of two. Viewing the number in binary, the player can distinguish all the primes as they are separated with a lot of $0$-bits. They can do so either programmatically or by hand.

## Description

- In the depths of an old tomb, a cryptic puzzle guarded a powerful relic. Many had attempted to break its code, but none had succeeded. This time, a daring cryptographer discovered a faint inscription on the wall—a clue, seemingly meaningless, about pairs and shadows of two. As they delved into the cipher, the hint began to make sense, guiding their steps through the labyrinth of numbers. But as the final secret unraveled, the crypt echoed with a low whisper: "Some things are better left in darkness." The relic was revealed, but the curse had only just begun.

## Skills Required

- Basic RSA knowledge.
- Learn how integers are represented in binary.

## Skills Learned

- Learn how to extract information from binary numbers.

# Enumeration

In this challenge we are provided with two files:

- `source.py` : This is the main script of the challenge that produces the output file.
- `output.txt` : This is the output file that contains the RSA parameters, the encrypted flag and the hint.

## Analyzing the source code

The source script is short so let us start by analyzing it.

```python
from Crypto.Util.number import getPrime, bytes_to_long
from math import prod

FLAG = open('flag.txt', 'rb').read()

primes = [getPrime(128) for _ in range(16)]

n = prod(primes)
e = 0x10001
m = bytes_to_long(FLAG)
c = pow(m, e, n)
treat = sum([primes[i]*2**(0x1337-158*(2*i+1)) for i in range(16)])

with open('output.txt', 'w') as f:
		f.write(f'{n = }\n')
		f.write(f'{e = }\n')
		f.write(f'{c = }\n')
		f.write(f'{treat = }\n')
```

As usually, the flag is read from `flag.txt` and encrypted with RSA. The public exponent is equal to the standard value `0x10001 = 65537` and the RSA public key along with the encrypted flag are written to the file. Moreover, a weird-looking hint based on the 16 primes is computed and outputted to the file.

# Solution

Let us start by analyzing the modulus. This modulus is not a standard one; it consists of 16 128-bit prime numbers which makes it 2048 bits long and therefore it is practically infeasible to be factorized. The only information that is left to process is the hint value `treat`.

## Finding the vulnerability

For brevity, let us denote the RSA primes as $p_0, p_1, ..., p_{15}$. The hint value can be expressed as:
$$
\text{hint} = 2^{4761} p_0 + 2^{4445}p_1 + 2^{4129}p_2 + ... + 2^{21}p_{15}
$$
We are given a linear combination of the RSA primes with coefficients being continuously decreasing powers of two. This is a pointer that we should probably start thinking in base 2 rather than base 10. One could try expressing the hint value in binary and notice some patterns but we will explain the process step by step. Let us take a random number, multiply it by a large power of two and view the binary form of the result.

```python
>>> a = 0xdead
>>> bin(a)
'0b1101111010101101'
>>> bin(2**60 * a)
'0b1101111010101101000000000000000000000000000000000000000000000000000000000000'
```

We can see that the number $a$ remained as is, but a lot of zeroes were appended, therefore creating some empty "space". Notice that the same would happen if we performed a left shift of $a$ by 60 bits.

```python
>>> bin(a << 60)
'0b1101111010101101000000000000000000000000000000000000000000000000000000000000'
```

Now, let us append another small random number by adding it to $2^{32} \cdot a$.

```python
>>> b = 0xbeef
>>> bin(b)
'0b1011111011101111'
>>> bin(2**60 * a + b)
'0b1101111010101101000000000000000000000000000000000000000000001011111011101111'
```

Again, $b$ remained as is and was appended to the end of the large number. Let us now simulate the way the hint value is calculated, by multiplying $b$ with a large power of 2, *but smaller than 60*.

```python
>>> bin(2**60*a+2**27*b)
'0b1101111010101101000000000000000001011111011101111000000000000000000000000000'
```

In binary level, this is how the addition works:
$$
2^{60} \cdot a& = 1101111010101101000000000000000000000000000000000000000000000000000000000000\\
2^{27} \cdot b& = 0000000000000000000000000000000001011111011101111000000000000000000000000000\\
\hline
\text{hint} &= 1101111010101101000000000000000001011111011101111000000000000000000000000000
$$
The upper $60-27 = 33$ bits of $b$ are $0$, therefore the value of $a$ remains the same after the addition.

In the case of our challenge, we know only the $\text{hint}$ value but as we see, expressing it in base two, it becomes trivial to distinguish $a,b$ as a lot of $0$-bits separate them.

Let us now express the hint value of the challenge in base two.

```
0b1100010011000010000101100101001011100001110110100000111100100000001101110010101110000010100001111100001000011001101110110001010100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000101101111011111011010010010101111111110110101111101100101011111111000000100100000110101010000110010000110100111000110010000110010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ... <REDACTED> ... 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000110000010110100001100010000011100000001011011110011001110101011100101000101100110000001101101111011011101001110011011000010110010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010001111111000001111001001001100010010010010010101011011000111010000100000101111101000111011111111000101011100111100010110000101000000000000000000000
```

The primes are 128 bits and we can distinguish them as a lot of $0$-bits separate them. For example, the first two are:

```
p_0 = 11000100110000100001011001010010111000011101101000001111001000000011011100101011100000101000011111000010000110011011101100010101

p_1 = 10110111101111101101001001010111111111011010111110110010101111111100000010010000011010101000011001000011010011100011001000011001
```

Since they are prime numbers, they must be odd so we know the last bit is always $1$, which makes it easy to distinguish them.

To extract all the primes, we can either start from the MSB or the LSB. To avoid making the process more complicated by performing large right shifts and `AND` operations, we will start from the LSB. The idea is trivial:

1. Start from the least significant bit and right shift by $1$ bit until the least significant bit becomes a $1$-bit.
2. In this case, we found a prime number so extract the last 128 bits and append to the list of primes. We can extract the last 128 bits of hint either by computing $\text{hint}\ \&\ (2^{128}-1)$ or $\text{hint} \pmod {2^{128}}$.
3. Remove the last 128 bits from hint by right shifting by 128 bits and go back to step 1 until the hint value becomes 0.

Let us perform the first iteration manually. The last bits of $\text{hint}$ are:

```
111111000001111001001001100010010010010010101011011000111010000100000101111101000111011111111000101011100111100010110000101000000000000000000000

Remove LSB : 
11111100000111100100100110001001001001001010101101100011101000010000010111110100011101111111100010101110011110001011000010100000000000000000000

Remove LSB : 1111110000011110010010011000100100100100101010110110001110100001000001011111010001110111111110001010111001111000101100001010000000000000000000

Remove LSB :
111111000001111001001001100010010010010010101011011000111010000100000101111101000111011111111000101011100111100010110000101000000000000000000

Remove LSB :
11111100000111100100100110001001001001001010101101100011101000010000010111110100011101111111100010101110011110001011000010100000000000000000

.
.
.

Remove LSB :
11111100000111100100100110001001001001001010101101100011101000010000010111110100011101111111100010101110011110001011000010100

Remove LSB :
1111110000011110010010011000100100100100101010110110001110100001000001011111010001110111111110001010111001111000101100001010

Remove LSB :
111111000001111001001001100010010010010010101011011000111010000100000101111101000111011111111000101011100111100010110000101

[+] Prime found :
111111000001111001001001100010010010010010101011011000111010000100000101111101000111011111111000101011100111100010110000101

// ... Extract and remove the last 128 bits and continue the process ...
```

Lt us write a python function that automates the prime extraction.

```python
def extract_primes(hint):
  	primes = []
    while hint:
        hint >>= 1
        if hint % 2 == 1:
            primes.append(hint & (2**128-1))
            hint >>= 128
		return primes
```

Having the primes, we can create a simple RSA decryption function.

```python
from math import prod

def decrypt(n, e, c, primes):
  	assert n == prod(primes)
    phi = prod([p-1 for p in primes])
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    return long_to_bytes(m)
```

## Getting the flag

A final recap of all that was said above:

1. Notice that among the RSA public key and the encrypted flag, we are also provided with a hint value.
2. This hint value is a linear combination of the RSA primes with the coefficients being continuously decreasing powers of two.
3. Viewing the hint value in binary, enables us to distinguish each of the primes as they are separated with a lot of $0$-bits.

This recap can be represented by code with the `pwn()` function:

```python
def pwn():
    primes = extract_primes(treat)
    flag = decrypt(n, e, c, primes)
    print(flag.decode())

if __name__ == '__main__':
		pwn()
```
