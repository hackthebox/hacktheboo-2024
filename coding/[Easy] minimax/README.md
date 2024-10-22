<img src="../../assets/banner.png" style="zoom: 80%;" align=center />

<img src="../../assets/logo.png" style="zoom: 80%;" align='left' /><font size="6">minimax</font>

1<sup>st</sup> October 2024

Prepared By: reva101

Challenge Author(s): reva101

Difficulty: <font color='green'>Easy</font>





# Synopsis

Given a string of numbers, find the smallest and largest and print them out.

## Skills Required
* Basic Python

# Solution
Parse the string into an array and then apply the `min` and `max` functions. 

The solve script is below:

```py
nums = [float(x) for x in input().split()]

print(min(nums))
print(max(nums))
```