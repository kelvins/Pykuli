# Pykuli

[![Travis](https://travis-ci.org/kelvins/Pykuli.svg?branch=master)](https://travis-ci.org/kelvins/Pykuli)
[![Coverage Status](https://coveralls.io/repos/github/kelvins/Pykuli/badge.svg?branch=master)](https://coveralls.io/github/kelvins/Pykuli?branch=master)
[![License: MIT](https://img.shields.io/badge/License-GPL-brightgreen.svg)](LICENSE)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)

Python package inspired by Sikuli. 

Pykuli is intended to be easier to use than Sikuli (at least in Python).

Pykuli should be used to automate processes when there is no easy way to access the GUI's or the source code.

# Dependencies

Some dependencies that you may need to install.

## PyUserInput Dependencies

Depending on your platform, you will need the following python modules for PyUserInput to function:

- Linux: Xlib
- Mac: Quartz, AppKit
- Windows: pywin32, pyHook

# Usage

```python
pykuli = Pykuli('imgs/')

pykuli.click('username_input.png')
pykuli.type_string('username')

pykuli.click('password_input.png')
pykuli.type_string('password')

pykuli.tap_key('return')
```

## License

This project is developed under the GPL-3.0 license.
Feel free to contribute in any way.