<img src="../../assets/banner.png" style="zoom: 80%;" align=center />

<img src="../../assets/logo.png" style="zoom: 80%;" align='left' /><font size="6">Oddly Even</font>

1<sup>st</sup> October 2024

Prepared By: ir0nstone

Challenge Author(s): ir0nstone

Difficulty: <font color='green'>Very Easy</font>

# Synopsis
Given a number, print "even" if it is even and "odd" if it is odd.

## Skills Required
* Basic Python

# Solution
First, we take in the number:

```py
a = int(input())
```

We can then check if the number is divisible by `2`. If it is, we print "even", otherwise we print "odd".

```py
if a % 2 == 0:
    print('even')
else:
    print('odd')
```