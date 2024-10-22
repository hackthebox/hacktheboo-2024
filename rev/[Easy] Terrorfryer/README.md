<img src="../../assets/banner.png" style="zoom: 80%;" align=center />

<img src="../../assets/logo.png" style="zoom: 80%;" align='left' /><font size="6">Terrorfryer</font>

  1<sup>st</sup> 10 24 / Document No. D24.102.166

  Prepared By: clubby789

  Challenge Author: clubby789

  Difficulty: <font color=green>Easy</font>

  Classification: Official






# Synopsis

Terrorfryer is a Easy reversing challenge. Players must reverse engineer a deterministic string shuffling function to find the flag.

## Skills Required
    - Basic decompiler usage
## Skills Learned
    - Leaking deterministic RNG

# Solution

Running the binary, we are prompted:

```
Please enter your recipe for frying:
```

Entering `abc123`, it seems that the string is shuffled and compared to another shuffled string.
```
got:      `12ab3c`
expected: `1_n3}f3br9Ty{_6_rHnf01fg_14rlbtB60tuarun0c_tr1y3`
This recipe isn't right :(
```

## Analysis

We'll decompile the binary.
```c
printf(format: "Please enter your recipe for frying: ")
char buf[0x40]
fgets(&buf, n: 0x40, fp: __TMC_END__)
char* nl = strchr(&buf, '\n')

if (nl != 0)
    *nl = 0

fryer(&buf)
printf(format: "got:      `%s`\nexpected: `%s`\n", &buf, desired)

if (strcmp(desired, &buf) == 0)
    puts(str: "Correct recipe - enjoy your meal!")
 else
    puts(str: "This recipe isn't right :(")
```

We read up to 0x40 bytes then call `fryer` (after removing the newline).

```c
uint64_t fryer(char* s) {
    if (init.1 == 0) {
        seed.0 = 0x13377331;
        init.1 = 1;
    }
    
    uint64_t tmp = strlen(s);
    uint64_t len = tmp;
    
    if (tmp > 1) {
        int64_t len_no_nul = (tmp - 1);
        int64_t i = 0;
        do {
            int32_t j = (rand_r(&seed.0)) % (len - i) + i;
            tmp = s[i];
            char* other = &s[j];
            s[i] = *other;
            *other = tmp;
            i += 1;
        } while (i != len_no_nul);
    }
    
    return tmp;
}

```

We begin by checking a global variable (`init.1`) then initialize the global `seed.0` to `0x13377331`.

We then loop from 0 to the length of the string (minus 1). This is a shuffling algorithm - those familiar with GNU libc internals may recognize it as a deterministic version of [strfry](https://man7.org/linux/man-pages/man3/strfry.3.html).

## Solving

We could attempt to reverse the RNG; however, we can analyze the binary output to simplify this. We'll write a script using `pwntools` to perform this.

We'll start by sending a string of unique characters. This will allow us to identify the shuffle order.
```py
from pwn import *
import string

r = process("./fryer")
inp = string.printable[:48]  # Length of expected input
r.sendlineafter(b"frying: ", inp.encode())
```

We'll then read out the shuffled result, and the expected output.

```py
r.recvuntil(b'`')
output = r.recvline()[:-2].decode()
r.recvuntil(b'`')
shuffled = r.recvline()[:-2].decode()
```

We can then iterate over each character in the input string and find the position it is located in the resulting string. By applying this mapping to the shuffled expected data, we can retrieve the flag.

```py
flag = ""
for c in inp:
    flag += shuffled[output.index(c)]
print(flag)
```
