from math import prod
from Crypto.Util.number import long_to_bytes

exec(open('output.txt').read())

def extract_primes(hint):
    primes = []
    while hint:
        hint >>= 1
        if hint % 2 == 1:
            primes.append(hint % 2**128)
            hint >>= 128
    return primes

def decrypt(n, e, c, primes):
    assert n == prod(primes)
    phi = prod([p-1 for p in primes])
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    return long_to_bytes(m)

def pwn():
    primes = extract_primes(treat)
    flag = decrypt(n, e, c, primes)
    print(flag.decode())

if __name__ == '__main__':
    pwn()