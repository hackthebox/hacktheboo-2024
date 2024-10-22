<img src="../../assets/banner.png" style="zoom: 80%;" align=center />

<img src="../../assets/logo.png" style="zoom: 80%;" align='left' /><font size="6">Graverobber</font>

  4<sup>th</sup> 10 24 / Document No. D24.102.X168

  Prepared By: clubby789

  Challenge Author: clubby789

  Difficulty: <font color=green>Very Easy</font>

  Classification: Official






# Synopsis

Graverobber is a Very Easy reversing challenge. Players will use `strace` to identify binary functionality, then scripting to uncover the flag.

## Skills Learned
    - strace
    - basic scripting


# Solution

If we run the provided binary, we're given an error message.

```
We took a wrong turning!
```

## Tracing

We can use `strace` to try and guess what the binary is doing.

```c
$ strace ./robber
/* SNIP */
newfstatat(AT_FDCWD, "H/", 0x7ffcbd70cf50, 0) = -1 ENOENT (No such file or directory)
write(1, "We took a wrong turning!\n", 25We took a wrong turning!
) = 25
exit_group(1)                           = ?
+++ exited with 1 +++
```

We're trying to use `newfstatat` (a specialized version of the `stat` syscall used for file metadata) on some directory `H`. If we create it and run again:

```c
newfstatat(AT_FDCWD, "H/", {st_mode=S_IFDIR|0755, st_size=4096, ...}, 0) = 0
newfstatat(AT_FDCWD, "H/T/", 0x7fff03f91e00, 0) = -1 ENOENT (No such file or directory)
write(1, "We took a wrong turning!\n", 25We took a wrong turning!
```

Looks like it will open several directories in sequence. We'll write a script to automate creating them.

## Scripting

We'll begin by deleting and creating a directory to work in.

```py
import os
import shutil
from pwn import *

try:
    shutil.rmtree("directories")
    os.mkdir("directories")
except Exception:
    pass
os.chdir("directories")
```

We'll then loop, running the binary under `strace` (using `-e` to filter to only the `newfstatat` calls):

```py
while True:
    with context.local(log_level='ERROR'):
        p = process(["strace", "-e", "newfstatat", "../robber"])
        out = p.recvall().decode()
        p.close()
```

We'll then look at the last call to see the last path expected, and use that to create a directory. We'll also break if the error message isn't printed as we've likely found the whole path.

```py
        if 'wrong turning' not in out: break
        stats = [line for line in out.split("\n") if "newfstatat" in line]
        # Get last line, and get the content of the string
        path = stats[-1].split('"')[1]
        # Remove separators and print path
        print(path.replace("/", ""))
        # Recursively make the directory
        os.makedirs(path)
```

On running this script, we'll get the flag.
