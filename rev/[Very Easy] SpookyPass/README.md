<img src="../../assets/banner.png" style="zoom: 80%;" align=center />

<img src="../../assets/logo.png" style="zoom: 80%;" align='left' /><font size="6">SpookyPass</font>

  4<sup>th</sup> 10 24 / Document No. D24.102.169

  Prepared By: clubby789

  Challenge Author: clubby789

  Difficulty: <font color=green>Very Easy</font>

  Classification: Official






# Synopsis

SpookyPass is a Very Easy reversing challenge. Players will use `strings` to identify a password.

## Skills Learned
    - `strings`

# Solution

Running the binary, we're given a password prompt:

```
Welcome to the SPOOKIEST party of the year.
Before we let you in, you'll need to give us the password: foo
You're not a real ghost; clear off!
```

We'll use `strings` to look for hidden data in the program:

```sh
$ strings ./pass
# .. SNIP ..
Welcome to the 
[1;3mSPOOKIEST
[0m party of the year.
Before we let you in, you'll need to give us the password: 
s3cr3t_p455_f0r_gh05t5_4nd_gh0ul5
Welcome inside!
You're not a real ghost; clear off!
# .. SNIP ..
```

If we try `s3cr3t_p455_f0r_gh05t5_4nd_gh0ul5` as the password, we'll be accepted and receive the flag.
