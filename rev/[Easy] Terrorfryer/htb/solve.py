#!/usr/bin/env python3

from pwn import *
import string

binary = args.BINARY or "./fryer"
r = process(binary)
inp = string.printable[:48]
r.sendlineafter(b"frying: ", inp.encode())
r.recvuntil(b'`')
output = r.recvline()[:-2].decode()
r.recvuntil(b'`')
shuffled = r.recvline()[:-2].decode()

flag = ""
for c in inp:
    flag += shuffled[output.index(c)]
print(flag)