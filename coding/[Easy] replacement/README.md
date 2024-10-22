<img src="../../assets/banner.png" style="zoom: 80%;" align=center />

<img src="../../assets/logo.png" style="zoom: 80%;" align='left' /><font size="6">Replacement</font>

1<sup>st</sup> October 2024

Prepared By: ir0nstone

Challenge Author(s): ir0nstone

Difficulty: <font color='green'>Easy</font>

# Synopsis
Given a string, a letter in the string and a random letter, replace all instances of the first letter with the latter.

## Skills Required
* Basic Python

# Solution
Take in the inputs and call `replace()`.

```py
s = input()
to_replace = input()
to_use = input()

print(s.replace(to_replace, to_use))
```