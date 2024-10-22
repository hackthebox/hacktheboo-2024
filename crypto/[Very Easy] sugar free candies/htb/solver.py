from sage.all import *
from Crypto.Util.number import long_to_bytes

exec(open('output.txt').read())

def create_variables():
    x,y,z = var('x,y,z', domain=ZZ)
    return x,y,z

def solve_system(x, y, z):
    return solve([
        x**3 + z**2 + y == v1,
        y**3 + x**2 + z == v2,
        z**3 + y**2 + x == v3,
        x + y + z == v4
    ], x, y, z, solution_dict=True)[0]

def get_flag(sols):
    return b''.join([long_to_bytes(int(n)) for n in [sols[x], sols[y], sols[z]]])

def pwn():
    x, y, z = create_variables()
    sols = solve_system(x, y, z)
    flag = get_flag(sols)
    print(flag)


if __name__ == '__main__':
    pwn()