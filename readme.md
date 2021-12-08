# Kalc

[![Python 3.6+](https://upload.wikimedia.org/wikipedia/commons/8/8c/Blue_Python_3.6%2B_Shield_Badge.svg)](https://www.python.org/downloads/release/python-360/)

[![Windows](https://svgshare.com/i/ZhY.svg)](https://github.com/Rygor83/kalc) [![Linux](https://svgshare.com/i/Zhy.svg)](https://github.com/Rygor83/kalc)

[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://choosealicense.com/licenses/mit/)

Windows/Linux Command line calculator. Allows making calculations of any complexity directly in the console.  
Linux: tested on Windows 10 with WSL Ubuntu and Pycharm.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```cmd
pip install <path to kalc folder>
```

## Usage

```
Usage: kalc [OPTIONS] EXPRESSION
  Evaluates the specified math expression

  EXPRESSION                      math expression

Options:
  -uf, --userfriendly    FLAG     User-friendly output. Separate thousands with a spaces
  -c,  --copytoclipboard FLAG     Copy results into clipboard
  -d,  --rounddecimal    INTEGER  Round a result up to <rounddecimal> decimal
  -config                FLAG     Open config
  --help                          Show this message and exit.
```

```
Examples: kalc (2+2)*2 <ENTER>
Text appearing in the console: 8

Example: kalc (2+2)*2=<ENTER>
Text appearing in the console: (2+2)*2=8

Example: kalc 1000000/3 -d 3 <ENTER>
Text appearing in the console: 333333.333

Example: kalc 1000000/3 -d 5 <ENTER>
Text appearing in the console: 333333.33333

Example: kalc 10**8 -uf <ENTER>
Text appearing in the console: 100 000 000.00

Example: kalc fsum([2,4,6,8,10,12]) <ENTER>
Text appearing in the console: 42.00

Example: kalc "3**2 + sin(pi/2) / exp(2)" <ENTER>
Text appearing in the console: 9.14
```

Hints:

- kalc module is not case-sensitive
- blanks in expressions are allowed only with quotes ( " " ):

```
kalc "2 + 2 - 1"
```

- decimal part must be separated by dot (not comma)
- expression must be written according to the common rules of writing math expression on a PC. For instance: x^2+sin(5*
  y)/exp(4*z)
- kalc module considers parenthesis ( i.e. '(' and ')' )
- kalc module knows the following operations:

| Operations                                                                                          | Description                             | Examples                     |
|:----------------------------------------------------------------------------------------------------|:----------------------------------------|:-----------------------------|
| **Basic
operations**                                                                                |                                         |                              |
| +                                                                                                   | addition                                | kalc 2+2 -> result 4        |
| -                                                                                                   | substraction                            | kalc 2-1 -> result 3        |
| /                                                                                                   | division                                | kalc 4/2 -> result 2        |
| *                                                                                                   | multiplication                          | kalc 3*3 -> result 9        |
| **                                                                                                  | exponentiation                          | kalc 3**2 -> result 9        |
| //                                                                                                  | floor division                          | kalc 6//4 -> result 1        |
| %                                                                                                   | modulus                                 | kalc 6%4 -> result 2        |
| **
Functions**                                                                                       |                                         |                              |
| sin                                                                                                 | sinus                                   | kalc sin(pi/2) -> result 1   |
| cos                                                                                                 | cosine                                  | kalc cos(pi)   -> result -1  |
| tan                                                                                                 | tangent                                 |                              |
| exp                                                                                                 | exponent                                | kalc exp(2) -> result 7.39   |
| log                                                                                                 | natural logarithm                       | kalc log(e) -> result 1      |
| sqrt                                                                                                | square root                             | kalc sqrt(121) -> result 121 |
| trunc                                                                                               | truncation                              | kalc trunc(7.35) -> result 7 |
| Other functions from python [math](https://docs.python.org/3/library/math.html) module is available |                                         |                              |
|                                                                                                     |                                         |                              |
| **Numeric
literals**                                                                                |                                         |                              |
| pi                                                                                                  | The mathematical constant π = 3.141592… |                              |
| e                                                                                                   | The mathematical constant e = 2.718281… |                              |
| tau                                                                                                 | The mathematical constant τ = 6.283185… |                              |
| **Comparison
Operators** Works only with quotes. Answers: 1 for True, 0 for False                   |                                         |                              |
| ==                                                                                                  | equal                                   | "2==2" -> result 1.00 (True) |
| !=                                                                                                  | not equal                               | "2!=2" -> result 0.00 (False)|
| \>                                                                                                  | more                                    | "2>1" -> result 1.00 (True)  |
| <                                                                                                   | less                                    | "2<2" -> result 0.00 (False) |
| > =                                                                                                  | more or equal                           | "2>=2" -> result 1.00 (True) |
| <=                                                                                                  | less or equal                           | "2<=2" -> result 1.00 (True) |

## Configuration

The kalc's default settings are stored in kalc_config.ini:

- Windows path: c:\Users\USERNAME\AppData\Local\kalc\
- Linux path: /home/USERNAME/.local/share/kalc

kalc's configuration file is created at the moment of first calculations.

To open config file for editing purpose run:

```
kalc -config
```

Config parameters
```
[General]
decimalround     - Round a result up to <decimalround> decimal. Values: integer.
copytoclipboard  - Need to copy results into clipboard. Values: True/False
userfriendly     - Need to separate thousands with a space. Values: True/False. Example: 1 000 000
```

Kalc's command options (-uf, -d, -c) have priority over configuration parameters.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)