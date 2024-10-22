![img](../../../../../assets/htb.png)

<img src='../../../../../assets/logo.png' style='zoom: 80%;' align=left /><font size='5'>brevi moduli</font>

​	25<sup>th</sup> September 2024 / Document No. D24.102.XX

​	Prepared By: `rasti`

​	Challenge Author(s): `rasti`

​	Difficulty: <font color=lightgreen>Very Easy</font>

​	Classification: Official



# Synopsis

- `brevi moduli` is a very easy challenge. The player has to pass five rounds to get the flag. At each round, they will have to submit the prime factors $p, q$ of a 220-bit RSA modulus. Since the modulus is small, it can be factored by most tools, such as SageMath.

## Description

- On a cold Halloween night, five adventurers gathered at the entrance of an ancient crypt. The Cryptkeeper appeared from the shadows, his voice a chilling whisper: "Five locks guard the treasure inside. Crack them, and the crypt is yours." One by one, they unlocked the crypt's secrets, but as the final door creaked open, the Cryptkeeper's eerie laughter filled the air. "Beware, for not all who enter leave unchanged."



## Skills Required

- Know how to interact with TCP servers using pwntools.
- Very basic knowledge of the RSA cryptosystem and the Integer Factorization problem.

## Skills Learned

- Learn how to factor small RSA moduli with SageMath (or any other tool).

# Enumeration

In this challenge, we are provided with just a single file:

- `server.py` : This is the python script that runs when we connect to the challenge instance.

## Analyzing the source code

Let us first analyze the server code. 

```python
rounds = 5
e = 65537

for i in range(rounds):
    print('*'*10, f'Round {i+1}/{rounds}', '*'*10)

    p = getPrime(110)
    q = getPrime(110)
    n = p * q
    pubkey = RSA.construct((n, e)).exportKey()
    print(f'\nCan you crack this RSA public key?\n{pubkey.decode()}\n')

    assert isPrime(_p := int(input('enter p = '))), exit()
    assert isPrime(_q := int(input('enter q = '))), exit()

    if n != _p * _q:
        print('wrong! bye...')
        exit()

    print()

print(open('flag.txt').read())
```

To get the flag, we have to pass 5 rounds successfully. At each round, we are provided with an RSA public key and the task is to provide the prime factors $p, q$ of the modulus $N$. The value of the public exponent, namely $e$, is fixed to the standardized value $65537$.

# Solution

## Finding the vulnerability

The security of the RSA cryptosystem, lies entirely on the hardness of solving the Integer Factorization problem. In simple words, this problem can be summarized as:

*Given $p = 10412581$ and $q = 15559549$, it is trivial and very fast to calculate that $10412581 \cdot 15559549 = 162015064285969 = N$. However, given only $N = 162015064285969$, it is much harder to find which two numbers $p,q$ were multiplied to produce it.*

For much larger numbers, it becomes infeasible for the modern computers to solve this problem.

In this challenge, the size of each prime is $110$ bits, so their product is $110 + 110 = 220$ bits in total. It turns out that a $220$-bit RSA modulus is totally insecure to use for cryptography as it can be factored by modern computers very fast. There are many libraries and tools that factor integers but in CTF challenges, the most commonly used is SageMath so we will stick with it. Let us see an example first with dummy numbers.

```python
sage: p = random_prime(2^110)
sage: q = random_prime(2^110)
sage: n = p * q
sage: %time factor(n)
CPU times: user 6.46 s, sys: 7.96 ms, total: 6.47 s
Wall time: 6.5 s
356113038545854871808945806883821 * 1270756668530534635604669619715399
sage: p
356113038545854871808945806883821
sage: q
1270756668530534635604669619715399
```

We can see it took only 6.5 seconds for SageMath to factor $n$. Therefore, our task is pretty clear:

Connect to the server, retrieve the modulus at each round, factor it and send the factors back to the server.

However, the RSA public key is provided to us in PEM format.

```python
pem_pubkey = RSA.construct((n, e)).exportKey()
print(f'\nCan you crack this RSA public key?\n{pubkey.decode()}\n')
```

The PEM format is as follows:

```
-----BEGIN PUBLIC KEY-----
MDcwDQYJKoZIhvcNAQEBBQADJgAwIwIcBEwL/SBkcv+AmVwzDWtY80vQ4ALwjtUt
RgeXuwIDAQAB
-----END PUBLIC KEY-----
```

One might wonder why do we have to use such a weird format for sending RSA public keys. The reason is that RSA is widely used in applications such as TLS, which means that the key format must be consistent to avoid errors while parsing the parameters. Conventionally, applications utilize the PEM format. If no such format is used, one could argue which of the following should be used:

- `(n = value_of_n, e = value_of_e)`
- `(n=value_of_n,e=value_of_e)`
- `[n=value_of_n, e=value_of_e]`

and so on.

The way to read the actual RSA parameters from a PEM formatted key is to use the inverse of `exportKey` which is `importKey`.

```python
>>> from Crypto.PublicKey import RSA
>>> n = 452533018482816403250499886919603981486991592917670642633077659579
>>> e = 65537
>>> pem_pubkey = RSA.construct((n, e)).exportKey()
>>> pem_pubkey
b'-----BEGIN PUBLIC KEY-----\nMDcwDQYJKoZIhvcNAQEBBQADJgAwIwIcBEwL/SBkcv+AmVwzDWtY80vQ4ALwjtUt\nRgeXuwIDAQAB\n-----END PUBLIC KEY-----'
>>> key = RSA.importKey(pem_pubkey)
>>> key
RsaKey(n=452533018482816403250499886919603981486991592917670642633077659579, e=65537)
```

## Exploitation

### Connecting to the server

We can finally move on and write a function that retrieves and factors the five moduli.

```python
from pwn import *
from Crypto.PublicKey import RSA
from sage.all import *

def get_flag():
    e = 65537
    for _ in range(5):
        io.recvuntil(b'key?\n')
        key = RSA.importKey(io.recvuntil(b'-----END PUBLIC KEY-----\n'))
        n, e = key.n, key.e
        p, q = list(factor(n))
        io.sendlineafter(b'p = ', str(p[0]).encode())
        io.sendlineafter(b'q = ', str(q[0]).encode())
        io.recvline()
    flag = io.recvline().strip().decode()
    return flag
```

### Getting the flag

A final summary of all that was said above:

1. Notice that the provided RSA public keys are small so they can be easily factored using SageMath.
2. Retrieve the public key of each round, factor it and send back the primes.
3. Repeat this five times to get the flag.

This recap can be represented by code with the `pwn()` function:

```python
def pwn():
  	flag = get_flag()
    print(flag)

if __name__ == '__main__':
    if args.REMOTE:
        host_port = sys.argv[1].split(':')
        HOST = host_port[0]
        PORT = host_port[1]
        io = remote(HOST, PORT, level='error')
    else:
        import os
        os.chdir('../challenge')
        io = process(['python3', 'server.py'], level='error')

    pwn()
```
