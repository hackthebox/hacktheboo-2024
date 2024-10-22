#!/usr/bin/python3
from pwn import *
import warnings
import os
warnings.filterwarnings('ignore')
context.log_level = 'critical'

fname = './que_onda' # Specifiy the binary name 

LOCAL = False        # Change it to "True" to run the solver locally

os.system('clear')   # Clear screen

if LOCAL:
  print('Running solver locally..\n')
  r    = process(fname)   # Starting local process
else:
  IP   = str(sys.argv[1]) if len(sys.argv) >= 2 else '0.0.0.0'
  PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 1337
  r    = remote(IP, PORT) # Opens a remote connection to the specified <IP> and <PORT> 
  print(f'Running solver remotely at {IP} {PORT}\n')

r.sendline('flag') # Sends the string "flag" to the remote instance

print(f'Flag --> {r.recvline_contains(b"HTB")[2:].strip().decode()}\n') # Reads the flag
