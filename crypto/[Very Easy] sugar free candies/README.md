![](assets/images/banner.png)

<img src="assets/images/htb.png" style="zoom: 80%;" align=left /><font size="5">sugar free candies</font>

​	22<sup>th</sup> September 2023 / Document No. D23.102.XX

​	Prepared by : `rasti`

​	Challenge Author(s): `0x50r4`

​	Difficulty: <font color=lightgreen>Very Easy</font>

​	Classification: Official

​		

 

# Synopsis

- `sugar free candies` is a very easy crypto challege. The flag of this challenge is splitted into three parts. Four relations between these splitted parts are calculated and outputted to an output text file. The players will have to solve a system of three unknowns, given four equations with SageMath, or any other tool of their choice, and recover the flag.

## Description

- For years, strange signals pulsed through the air on the eve of October 31st. Some said it was the voice of an ancient witch, others believed it was a message from something far darker. A cryptic message, scattered in three parts, was intercepted by a daring group of villagers. Legend spoke of a deal made between the witch and a shadowy figure, but the true intent of their secret could only be revealed by those brave enough to decipher it before midnight, when the veil between worlds would thin.



## Skills Required

- Basic Python source code analysis.
- Know how to work with equations with multiple variables programmatically.

## Skills Learned

- Solve equations with SageMath.

# Enumeration

In this challenge we are provided with two files.

- `source.py` : It is the main python script that produces the output file.
- `output.txt` : Contains the data outputted from the source script.

## Analyzing the challenge

The code of the script is not lengthy so let us take a look.

```python
from Crypto.Util.number import bytes_to_long

FLAG = open("flag.txt", "rb").read()

step = len(FLAG) // 3
candies = [bytes_to_long(FLAG[i:i+step]) for i in range(0, len(FLAG), step)]

cnd1, cnd2, cnd3 = candies

with open('output.tcnd1t', 'w') as f:
    f.write(f'v1 = {cnd1**3 + cnd3**2 + cnd2}\n')
    f.write(f'v2 = {cnd2**3 + cnd1**2 + cnd3}\n')
    f.write(f'v3 = {cnd3**3 + cnd2**2 + cnd1}\n')
    f.write(f'v4 = {cnd1 + cnd2 + cnd3}\n')
```

The steps can be summarised as:

- The challenge reads the flag from `flag.txt`, which is secret and not provided to us
- It is splitted in three parts, which are denoted as `cnd1`, `cnd2`, and `cnd3` respectively. Each part is then converted into an integer representation.
- Four relations between the splitted parts are calculated and finally outputted to the output file `output.txt`.

# Solution

Our task is straight forward. We have to solve a system of three unknowns given four equations. Since the number of unknowns is less than the number of equations we are given, it is guaranteed that a solution $(x, y, z) = (x_0, y_0, z_0)$ exists. It should be noted that three equations would also guarantee a unique solution.

However, the problem is that the numbers are large and the equations non-linear so it would be very hard to solve with just pen and paper. We have to use some tool for this purpose. By researching the keywords `python solve equations` with the search engine of your choice, one should stumble upon the `SymPy` library. However, as the SageMath library is more common in CTFs, we will prefer that one. Note that there are also online equation solvers that should work too.

# Exploitation

Let us first load the data from the output file.

```python
exec(open('output.txt').read())
```

Let us first write a function that creates and returns three variables, one for each part of the flag. Due to use of `bytes_to_long`, we know they must be integers so we care only about solutions in the set of integers $\mathbb{Z}$. In SageMath, we can define variables using the `var()` function.

```python
from sage.all import *

def create_variables():
		x,y,z = var('x,y,z', domain=ZZ)
    return x,y,z
```

Then, we move on solving the system. For this purpose, we will utilize SageMath's [function](https://doc.sagemath.org/html/en/reference/calculus/sage/symbolic/relation.html#sage.symbolic.relation.solve) `solve()`. This functions receives a list of equations and the variables we want to solve for. Let us write a function that returns the solutions of the equations.

```python
def solve_system(x, y, z, v1, v2, v3, v4):
		return solve([
                	x**3 + z**2 + y == v1,
                  y**3 + x**2 + z == v2,
                  z**3 + y**2 + x == v3,
                  x + y + z == v4
                ], x, y, z, solution_dict=True)[0]
```

We also choose to retrieve the solutions in a dictionary format, to make the solution parsing more convenient.

Having the solutions, we can reconstruct the flag as:

```python
from Crypto.Util.number import long_to_bytes

def get_flag(sols):
		return b''.join([long_to_bytes(int(n)) for n in [sols[x], sols[y], sols[z]]])
```

## Getting the flag

Let us recap the steps for getting the flag.

- We noticed the flag is splitted into three parts.
- We noticed that we are given four relations of these parts so the system must have a unique solution.
- By minimal research, we see that we can solve systems using SageMath, SymPy or any online tool.
- Solving for the three unknown parts, we reconstruct the flag.

This recap can be represented with code as below:

```python
exec(open('output.txt').read())

def pwn():
    x, y, z = create_variables()
    sols = solve_system(x, y, z)
    flag = get_flag(sols)
    print(flag)


if __name__ == '__main__':
		pwn()
```

