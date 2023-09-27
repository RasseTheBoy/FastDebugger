# Changelog

## [0.0.41] - 2023-9-27

### Added

- Can now read [benedict](https://pypi.org/project/python-benedict/) types
    - `benedict` is a dictionary that can handle nested dictionaries
- New input variable for `__call__`
    - `exit: bool`
    - default: `False`
    - Exits the program after printing the debug message
- Updated and added new dostrings to all functions and classes in `fast_debugger.py`
- You can now import the FastDebugger class, instead of only importing `fd`; shown below

```py
from FastDebugger import FastDebugger

fd = FastDebugger()
```

### Changed

- The `config()` function handles `**kwargs` differently
    -  It was badly implemented before, and now it's fixed
- Input parameters removed from the `call()` function, and replaced with `**kwargs`
    - The available `**kwargs` parameters are found in the `__call__` function docstring

## [0.0.40] - 2023-4-4

### Added

- New input variable for `__call__`
    - `nl_end: bool`
    - default: `True`
    - Prints a new line at the end of the debug print
- New function: `config()`
    - Can configure some settings by giving the right input variables to a `**kwargs` (e.g. `fd.config(nl_end=False)`)
- New class `try_traceback`
    - Removed import statement `from py_basic_commands import try_traceback` and added as a class instead
    - Now you don't need install `py_basic_commands` to use `FastDebugger`
- Docstrings added to all functions and classes in `fast_debugger.py`
- Test code added to `fast_debugger.py`
    - Can be run by running `python fast_debugger.py` in the terminal
- Shields added to [README.md](readme.md)
    - Latest version
    - Status
    - Working Python versions
    - License

### Changed

- Main file renamed `FastDebugger.py` to `fast_debugger.py`
    - Importing still works the same way: `from FastDebugger import fd`
- Fixed` __init__.py` file
    - Now it imports `fast_debugger.py` instead of `FastDebugger.py`
    - And instead of importing the file `FastDebugger`, it imports the variable `fd`

## [0.0.31] - 2023-1-9

### Changed

- `__call__`
    - Uncommented the `try_traceback` decorator

## [0.0.3] - 2023-1-9

### Added

- Docstring to `FastDebugger` class and it's `__call__` function

## [0.0.2] - 2023-1-7

### Added

- `enabled` variable
    - if `True`, prints
    - if `False`, won't print

### Changed

- Completely changed how to the variable name is retrieved

## [0.0.1] - 2023-1-7

### Released

- Github created and package added to PyPi