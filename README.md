FastDebugger
==================

<p align="center">
    <img src="https://raw.githubusercontent.com/RasseTheBoy/FastDebugger/main/Logo/fast_debugger_logo.png" width=300>
</p>

FastDebugger is a debugging tool for Python that allows users to quickly and easily print the values of variables in their code. To use FastDebugger, users simply call the `fd()` function and pass it the variables they want to print. FastDebugger will then print the variable name, value and [other useful information](#how-to-use). This can be helpful for quickly checking the values of variables and troubleshooting code.

# Contents

- [Author](#author)
- [Installation](#installation)
- [How to use](#how-to-use)
    - [Basic example](#basic-example)
    - [Lists, sets, tuples and dictionarys](#lists-sets-tuples-and-dictionarys)
    - [Numpy arrays](#numpy-arrays)

# Author

- [@RasseTheBoy](https://github.com/RasseTheBoy)



# Installation

Install using pip

```bash
  pip install FastDebugger

  pip3 install FastDebugger
```

# How to use

## Basic example

### Input:
```py
from FastDebugger import fd

def foo(x, y, z):
    result = x + y + z
    fd(x, y, z, result)

foo(1, 2, 3)
```

### Output:
```py
fd |  int  | x: 1
fd |  int  | y: 2
fd |  int  | z: 3
fd |  int  | result: 6
```

### Output format:
```
fd | {variable type} | {variable name}: {variable value}
```

## Lists, sets, tuples and dictionarys

### Input:
```py
from FastDebugger import fd
from random import randint

def bar(n):
    lst = [randint(0, n) for _ in range(n)]
    dct = {f'key_{i}': randint(0, n) for i in range(n)}
    tpl = tuple(randint(0, n) for _ in range(n))
    st = {randint(0, n) for _ in range(n)}

    fd(lst, st, tpl, dct, nl=True)

bar(5)
```

### Output:
```py
fd |  list |  5  | lst
 ╟ |  int  |  0  | 4
 ╟ |  int  |  1  | 5
 ╟ |  int  |  2  | 3
 ╟ |  int  |  3  | 5
 ╚ |  int  |  4  | 4

fd |  set  |  3  | st
 ╟ |  int  |  0  | 0
 ╟ |  int  |  1  | 2
 ╚ |  int  |  2  | 3

fd | tuple |  5  | tpl
 ╟ |  int  |  0  | 3
 ╟ |  int  |  1  | 5
 ╟ |  int  |  2  | 0
 ╟ |  int  |  3  | 3
 ╚ |  int  |  4  | 5

fd |  dict |  5  | dct
 ╟ |  int  |  0  | key_0: 0
 ╟ |  int  |  1  | key_1: 1
 ╟ |  int  |  2  | key_2: 1
 ╟ |  int  |  3  | key_3: 0
 ╚ |  int  |  4  | key_4: 3
```

### Output format (list, set, tuple):
```
fd | {array type} | {array length} | {array name}
 ╚ | {variable type} | {index in array} | {variable value}
```

### Output format (dictionary):
```
fd | dict | {dict length} | {dict name}
 ╚ | {value type} | {index in dict} | {key}: {value}
```

## Numpy arrays

### Input:
```py
from FastDebugger import fd
import numpy as np

def bar(a, b):
    c = a * b
    d = np.sin(c)
    e = np.cos(d)
    f = np.tan(e)
    fd(a, b, c, d, e, f, nl=True)

bar(np.array([1, 2, 3]), np.array([4, 5, 6]))
```

### Output:
```py
fd | ndarray |  3  | a
 ╟ | int32 |  0  | 1
 ╟ | int32 |  1  | 2
 ╚ | int32 |  2  | 3

fd | ndarray |  3  | b
 ╟ | int32 |  0  | 4
 ╟ | int32 |  1  | 5
 ╚ | int32 |  2  | 6

fd | ndarray |  3  | c
 ╟ | int32 |  0  | 4
 ╟ | int32 |  1  | 10
 ╚ | int32 |  2  | 18

fd | ndarray |  3  | d
 ╟ | float64 |  0  | -0.7568024953079282
 ╟ | float64 |  1  | -0.5440211108893698
 ╚ | float64 |  2  | -0.7509872467716762

fd | ndarray |  3  | e
 ╟ | float64 |  0  | 0.7270351311688124
 ╟ | float64 |  1  | 0.8556343548213666
 ╚ | float64 |  2  | 0.7310155667453406

fd | ndarray |  3  | f
 ╟ | float64 |  0  | 0.8895922779758605
 ╟ | float64 |  1  | 1.1513517113559995
 ╚ | float64 |  2  | 0.8967481047747234
```

### Output format (exactly like lists, sets...):
```
fd | {array type} | {array length} | {array name}
 ╚ | {variable type} | {index in array} | {variable value}
```
