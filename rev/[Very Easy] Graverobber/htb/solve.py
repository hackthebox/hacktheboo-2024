#!/usr/bin/env python3
import os
import shutil
from pwn import *

try:
    shutil.rmtree("directories")
    os.mkdir("directories")
except Exception:
    pass
os.chdir("directories")

while True:
    with context.local(log_level='ERROR'):
        p = process(["strace", "-e", "newfstatat", "../robber"])
        out = p.recvall().decode()
        p.close()
        if 'wrong turning' not in out: break
        stats = [line for line in out.split("\n") if "newfstatat" in line]
        path = stats[-1].split('"')[1]
        print(path.replace("/", ""))
        os.makedirs(path)

