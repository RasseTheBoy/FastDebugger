# Changelog

## [0.0.32] - 2023

### Added

- New input variable for `__call__`
    - `nl_end: bool`
    - default: `True`
    - Prints a new line at the end of the debug print
- New function: `config()`
    - Can configure some settings by giving the right input variables to a **kwars

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