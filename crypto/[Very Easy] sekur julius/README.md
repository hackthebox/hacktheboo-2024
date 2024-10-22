![img](../../../../../assets/htb.png)

<img src='../../../../../assets/logo.png' style='zoom: 80%;' align=left /><font size='5'>sekur julius</font>

​	2<sup>nd</sup> October 2024 / Document No. D24.102.XX

​	Prepared By: `rasti`

​	Challenge Author: `rasti`

​	Difficulty: <font color=lightgreen>Very Easy</font>

​	Classification: Official

# Synopsis

- `sekur julius` is a very easy crypto challenge. The player has to understand that no matter how many times Caesar cipher is applied to a message, the security does not increase as each character is shifted by the same shift offset each time. Therefore, 1337 Caesar encryptions are equivalent to that of a single one. The task is to perform Caesar cipher decryption to obtain the flag string and wrap it with the usual HTB flag format `HTB{}`.

## Description

- Hidden deep in the forest was an ancient scroll, rumored to grant immense power to anyone who could read its shifting symbols. On Halloween, a curious traveler found the scroll, its letters strangely out of order. As they deciphered the message, the words slowly rearranged themselves, revealing a dark spell. But with the final shift, the traveler felt a cold presence behind them, whispering, "You were never meant to understand." The forest grew silent, but the spell was already cast.

## Skills Required

- Basic knowledge of the Caesar cipher

## Skills Learned

- Learn that performing several encryptions with Caesar cipher does not increase the security.

# Enumeration

In this challenge we are provided with two files:

- `source.py` : This is the script that encrypts the secret message and writes the ciphertext to `output.txt`
- `output.txt` : This is the output file that contains the encrypted message

## Analyzing the source code

Let us first analyze the source of the script.

```python
from random import choices

def julius_encrypt(msg, shift):
    ct = ''
    for p in msg:
        if p == ' ':
            ct += '0'
        elif not ord('A') <= ord(p) <= ord('Z'):
            ct += p
        else:
            o = ord(p) - 65
            ct += chr(65 + (o + shift) % 26)
    return ct

def encrypt(msg, key):
    for shift in key:
        msg = julius_encrypt(msg, shift)
    return msg

msg = open('secret.txt').read().upper()
secure_key = os.urandom(1337)

with open('output.txt', 'w') as f:
    f.write(encrypt(msg, secure_key))
```

The flow is very simple to follow. A message is read from `secret.txt` and is encrypted with a key. The key is a random byte string of 1337 bytes.

The message is then encrypted using each of these bytes as a key. The function that encrypts the actual message is called `julius_encrypt` and we are given its source code. The function iterates over each message character and encrypts it as follows:

1. If the character is a whitespace, it appends a '$0$' to the ciphertext
2. If the character is any other non-uppercase character, it appends it as it is.
3. If the character is in uppercase, it is substituted with the character being $\text{shift}$ positions to the right. For example, the letter 'A' with a key of 4 would have been encrypted to 'E'.

This encryption process should remind us of the Caesar Cipher and in this case the function name is a hint to verify our educated guess.

# Solution

## Finding the vulnerability

Caesar cipher is known to be vulnerable due to its small key space, which in this challenge consists of a total of 26 characters; the uppercase English alphabet. However, there is a twist in this challenge; the message is not encrypted with a single shift but with 1337 shifts where each shift can be any number in the range $[0, 255]$.

A standard choice of a shift would be in the range $[0, 25]$ and not in $[0, 255]$. However, the encryption methods adds the shift to the plaintext letter and then reduces the result $\pmod {26}$.

```python
(o + shift) % 26
```

Due to the properties of modular arithmetic, this is equivalent too:

```python
(o % 26 + shift % 26) % 26
```

We observe no matter how large `shift` is, the final number will lie in the range $[0, 25]$. For example, encrypting with $\text{shift} = 250$ is equivalent to $250 \pmod {26} = 10$. As a result, we conclude that the effective keyspace of the cipher remains exactly the same.

Now, regarding the several rounds of encryption, let us see what happens if we encrypt a message with caesar two times, with two different shifts. Let the message `CRYPTOGRAPHY`. First, we encrypt the plaintext with a shift value of $3$, and then we encrypt the result with a shift value of $5$.
$$
\text{Plaintext} :& \text{C R Y P T O G R A P H Y}\\
\text{Shift by 3} :& \text{F U B S W R J U D S K B}\\
\text{Shift by 5} :& \text{K Z G X B W O Z I X P G}
$$
Notice that we can get the final result by encrypting the initial plaintext with a shift value equal to the sum of the sub-shifts; that is $3 + 5 = 8$.
$$
\text{Plaintext} :& \text{C R Y P T O G R A P H Y}\\
\text{Shift by 8} :& \text{K Z G X B W O Z I X P G}
$$
This is crucial as we eliminated one round of encryption and yet ended up with the same result. Back to our challenge, the secret message is encrypted with 1337 rounds. Similarly, we can obtain the final ciphertext by encrypting the message with the shift being the sum of all the 1337 sub-shifts, reduced $\pmod {26}$.  In the end, the effective shift value is again a number in the range $[0, 25]$.

The solution plan is trivial. All we have to do is decrypt the ciphertext with all 26 possible shift values and check if the plaintext looks like English language. We could use the index of coincidence technique to find the correct plaintext directly but it is not mandatory in this case.

Let us write a function that decrypts the ciphertext with all possible 26 keys.

```python
def decrypt():
		enc = open('output.txt').read()
    for i in range(1, 26):
    		print(f'{i = } | {julius_decrypt(enc, i)}')
```



## Getting the flag

A final summary of all that was said above:

1. Notice that the provided cipher is identical to the Caesar cipher.
2. Figure out that the "twist" of the shift values being in the range $[0, 255]$ does not add something to the security of the cipher and the keyspace remains the same.
3. With simple logic and experimentations, one can conclude that the total number of encryption rounds eventually drops down to a single encryption with Caesar cipher.
4. Knowing that, we can decrypt the ciphertext with all the possible 26 keys and check which result looks like English language.

This recap can be represented by code with the `pwn()` function:

```python
def pwn():
		decrypt()
  
pwn()
```
