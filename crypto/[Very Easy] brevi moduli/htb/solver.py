from pwn import *
from Crypto.PublicKey import RSA
from sage.all import *

io = None

def get_flag():
    e = 65537
    for _ in range(5):
        io.recvuntil(b'Round ')
        print(io.recvline().split()[0].decode())
        io.recvuntil(b'?\n')
        key = RSA.importKey(io.recvuntil(b'-----END PUBLIC KEY-----\n'))
        n, e = key.n, key.e
        p, q = list(factor(n))
        io.sendlineafter(b'pumpkin = ', str(p[0]).encode())
        io.sendlineafter(b'pumpkin = ', str(q[0]).encode())
        io.recvline()
    flag = io.recvline().strip().decode()
    return flag


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