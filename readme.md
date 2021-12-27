# Kalc

[![Python 3.6+](docs/resources/images/Python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)

[![Windows](docs/resources/images/os-windows-green.svg)](https://github.com/Rygor83/kalc) [![Linux](docs/resources/images/os-linux-green.svg)](https://github.com/Rygor83/kalc)

[![GitHub license](docs/resources/images/license-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Windows/Linux Command line calculator. Allows making calculations of any complexity directly in the console. Expandable
via plugins.

Linux: tested on Windows 10 with WSL Ubuntu and Pycharm.

## Installation

1. Download source code (Code -> Download ZIP) and extract to folder.
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```cmd
>>> pip install <path to kalc folder>
```

## Usage

```
Usage: kalc [OPTIONS] EXPRESSION
  Evaluates the specified math expression

  EXPRESSION                      math expression

Options:
  -uf, --userfriendly    BOOLEAN  User-friendly output. Separate thousands with a spaces
  -c,  --copytoclipboard          Copy results into clipboard
  -d,  --rounddecimal    INTEGER  Round a result up to <rounddecimal> decimal
  -ff, --free_format              Enter float numbers in any format (11.984,01; 11,984.01; 11984,01; 11984.01)
  -f, --function LIST / FUNCTION NAME
  -config                         Open config file
  -install, --plugin_install <PATH TO *.KALC FILE> 
                                  Install plugins into plugins folder
  -user                           Open user folder
  --version                       Show the version and exit.
  -l, --log_level LVL             Either CRITICAL, ERROR, WARNING, INFO or DEBUG
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

Example: kalc 12.435,84*20/120 -ff <ENTER>
Text appearing in the console: 2 072.64
```

Hints:

- kalc module is not case-sensitive
- blanks in expressions are allowed only with quotes ( " " ):

```
>>> kalc "2 + 2 - 1"
3.00
>>> kalc "fsum([1, 2, 3])"
6.00
```

- by default decimal part must be separated by dot (not comma). But if you use option -ff then decimal part can be in
  any format (11.984,01; 11,984.01; 11984,01; 11984.01)

```
>>> kalc 11.984,01+11,984.01+11984,01+11984.01 -ff
47 936.04
```

- expression must be written according to the common rules of writing math expression on a PC. For instance: x^2+sin(5*
  y)/exp(4*z)
- kalc module considers parenthesis ( i.e. '(' and ')' )
- kalc module knows the following operations:

| Operations                                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                    | Examples                     |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------|
| **[Basic operations](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)**                                                                                                                                                                                                                             |                                                                                                                                                |                              |
| +                                                                                                                                                                                                                                                                                                                                     | addition                                                                                                                                       | kalc 2+2 -> result 4         |
| -                                                                                                                                                                                                                                                                                                                                     | substraction                                                                                                                                   | kalc 2-1 -> result 3         |
| /                                                                                                                                                                                                                                                                                                                                     | division                                                                                                                                       | kalc 4/2 -> result 2         |
| *                                                                                                                                                                                                                                                                                                                                     | multiplication                                                                                                                                 | kalc 3*3 -> result 9         |
| **                                                                                                                                                                                                                                                                                                                                    | exponentiation                                                                                                                                 | kalc 3**2 -> result 9        |
| //                                                                                                                                                                                                                                                                                                                                    | floor division                                                                                                                                 | kalc 6//4 -> result 1        |
| %                                                                                                                                                                                                                                                                                                                                     | modulus                                                                                                                                        | kalc 6%4 -> result 2         |
| **Functions**                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                |                              |
| sin                                                                                                                                                                                                                                                                                                                                   | sinus                                                                                                                                          | kalc sin(pi/2) -> result 1   |
| cos                                                                                                                                                                                                                                                                                                                                   | cosine                                                                                                                                         | kalc cos(pi)   -> result -1  |
| tan                                                                                                                                                                                                                                                                                                                                   | tangent                                                                                                                                        |                              |
| exp                                                                                                                                                                                                                                                                                                                                   | exponent                                                                                                                                       | kalc exp(2) -> result 7.39   |
| log                                                                                                                                                                                                                                                                                                                                   | natural logarithm                                                                                                                              | kalc log(e) -> result 1      |
| sqrt                                                                                                                                                                                                                                                                                                                                  | square root                                                                                                                                    | kalc sqrt(121) -> result 121 |
| trunc                                                                                                                                                                                                                                                                                                                                 | truncation                                                                                                                                     | kalc trunc(7.35) -> result 7 |
| Other functions from python [math](https://docs.python.org/3/library/math.html) module is available                                                                                                                                                                                                                                   |                                                                                                                                                |                              |
| **Numericc literals**                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                |                              |
| pi                                                                                                                                                                                                                                                                                                                                    | The mathematical constant π = 3.141592…                                                                                                        |                              |
| e                                                                                                                                                                                                                                                                                                                                     | The mathematical constant e = 2.718281…                                                                                                        |                              |
| tau                                                                                                                                                                                                                                                                                                                                   | The mathematical constant τ = 6.283185…                                                                                                        |                              |
| **[Comparison operators](https://docs.python.org/3/reference/expressions.html#value-comparisons)** Works only with quotes. Answers: True, False                                                                                                                                                                                       |                                                                                                                                                |                              |
| ==                                                                                                                                                                                                                                                                                                                                    | equal                                                                                                                                          | "2==2" -> result True        |
| !=                                                                                                                                                                                                                                                                                                                                    | not equal                                                                                                                                      | "2!=2" -> result False       |
| \>                                                                                                                                                                                                                                                                                                                                    | more                                                                                                                                           | "2>1" -> result True         |
| <                                                                                                                                                                                                                                                                                                                                     | less                                                                                                                                           | "2<2" -> result False        |
| > =                                                                                                                                                                                                                                                                                                                                   | more or equal                                                                                                                                  | "2>=2" -> result True        |
| <=                                                                                                                                                                                                                                                                                                                                    | less or equal                                                                                                                                  | "2<=2" -> result True        |
| **[Shifting](https://docs.python.org/3/reference/expressions.html#shifting-operations) [Unary](https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations) and [binary](https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations) bitwise operators** Works only with quotes. |                                                                                                                                                |                              |
| <<                                                                                                                                                                                                                                                                                                                                    | left shift                                                                                                                                     | "10 << 1" -> 20              |
| \>>                                                                                                                                                                                                                                                                                                                                   | right shift                                                                                                                                    | "10 >> 1" -> 5               |
| &#124;                                                                                                                                                                                                                                                                                                                                | or                                                                                                                                             | "10 &#124; 1" -> 11          |
| &                                                                                                                                                                                                                                                                                                                                     | and                                                                                                                                            | "10 & 1" -> 0.00             | 
| ^                                                                                                                                                                                                                                                                                                                                     | xor                                                                                                                                            | "10 ^ 1" -> 11.00            |
| ~                                                                                                                                                                                                                                                                                                                                     | invert                                                                                                                                         | "~10" -> 11.00               |
| **[Boolean operations](https://docs.python.org/3/reference/expressions.html#boolean-operations)** Works only with quotes.                                                                                                                                                                                                             |                                                                                                                                                |                              |
| and                                                                                                                                                                                                                                                                                                                                   | The expression x and y first evaluates x; if x is false, its value is returned; otherwise, y is evaluated and the resulting value is returned. | "1 and 0" -> 0.00            |
| or                                                                                                                                                                                                                                                                                                                                    | The expression x or y first evaluates x; if x is true, its value is returned; otherwise, y is evaluated and the resulting value is returned.   | "1 or 0" -> 1.00             |
| not                                                                                                                                                                                                                                                                                                                                   | The operator not yields True if its argument is false, False otherwise.                                                                        | "not 1" -> 0.00              |
|                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                | "not 0" -> 1.00              |

## Configuration

The kalc's default settings are stored in kalc_config.ini:

- Windows path: c:\Users\USERNAME\AppData\Local\kalc\
- Linux path: /home/USERNAME/.local/share/kalc

kalc's configuration file is created at the moment of first calculations.

To open conf file for editing purpose run:

```
>>> kalc -conf
```

Config parameters

```
[General]
decimalround     - Round a result up to <decimalround> decimal. Values: integer.
copytoclipboard  - Need to copy results into clipboard. Values: True/False
userfriendly     - Need to separate thousands with a space. Values: True/False. Example: 1 000 000
free_format      - Can use free format of float ((11.984,01; 11,984.01; 11984,01; 11984.01)). Values: True/False
                   **Side effects**: if you use free_format parameter from conf file then use functions with multiple 
                   values carefully. For example FSUM([1,2,3,4,5,6,7,8,9,10]) will convert values 1,2,3,4,5,6,7,8,9,10
                   into 123456789.10. You have to delimite values with space and use quotes: 
                   "FSUM([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"  
```

Kalc's command options (-uf, -d, -c, -ff) have priority over configuration parameters.

If is possible open user folder with the followin command

```
>>> kalc -user
```

## Help on available functions and constants

Options:
-f, --function LIST / FUNCTION NAME Available functions help

It is possible to take a look at available functions and constants. Both for math module and for available plugins

```
>>> kalc -f list
List of available functions
1. Plugins:
Functions: compound_interest, sinterest
Constants: root2
2. Math module:
Functions: acos, acosh, asin, asinh, atan, atan2, atanh, ceil, comb, copysign, cos, cosh, degrees, dist, erf, erfc, exp, expm1, fabs, factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, isclose, isfinite, isinf, isnan, isqrt, lcm, ldexp, lgamma, log, log10, log1p, log2, modf, nextafter, perm, pow, prod, radians, remainder, sin, sinh, sqrt, tan, tanh, trunc, ulp
Constants: e, inf, nan, pi, tau
```

If you need help on any of available function:

```
>>> kalc -f sqrt
Return the square root of x.
```

```
>>> kalc -f pi
pi = 3.141592653589793
```

```
>>> kalc -f percent
Simple interest is a method to calculate the amount of interest charged on a principal amount at a given rate of interest and for a given period of time

:param percent: Rate of interest, for example 12
:param base_amount: Principal amount, for example 1000000
:param days_in_month: Days in given period of time, for example: 1 month = 30 days
:param days_in_year: Days in year, for example, 360/365/366
:return: Maturity amount
```


## Plugins

You can extend kalc with plugins

You need to create 2 files in any place you like:

1. Plugin Info File Format with 'kalc' extension (for example, myplugin.kalc):
   The plugin info file is a text file encoded in ASCII or UTF-8 and gathering, as its name suggests, some basic
   information about the plugin.
    * it gives crucial information needed to be able to load the plugin
    * it provides some documentation like information like the plugin author’s name and a short description fo the
      plugin functionality.

   Here is an example of what such a file should contain:

```
[Core]
Name = My plugin Name
Module = the_name_of_the_source_of_the_plugin_to_load_with_no_py_ending. In our case - myplugin
   
[Documentation]
Description = What my plugin broadly does
Author = My very own name
Version = the_version_number_of_the_plugin
Website = My very own website
```

2. The source of the plugin with 'py' extension (for example, myplugin.py):
   Here is an example of what such a file should contain:

```
from yapsy.IPlugin import IPlugin   # obligatory import of IPlugin

class PluginOne(IPlugin):           # define class that will contain functions (methods)
    """ Custom defined plugin with constants and functions """
    
    # Constants
    root2 = 1.41421356237309504880168872420969808  # Pythagoras' constant. The square root of 2, often known as root 2, radical 2, or Pythagoras' constant

	# Functions
    def percent(self, percent, base_amount, days_in_month: int = 30, days_in_year: int = 360):
        """
        Calculate percnet amount with the following parameters

        :param percent: Rate of interest, 12
        :param base_amount: Principal amount
        :param days_in_month: Days in period
        :param days_in_year: Days in year
        :return: Maturity amount
        """
        return base_amount * percent * days_in_month / days_in_year / 100

```

Then we need to install plugins into plugin directory - run the following command

```
>>> kalc -install <path to myplugin.kalc file>
Plugin "MYPLUGIN.KALC" is installed into "c:\Users\USERNAME\AppData\Local\kalc\plugins" folder - for windows
Plugin "MYPLUGIN.KALC" is installed into "/home/USERNAME/.local/share/kalc" folder - for Linux
```

Now you can use new functions and constants from plugin:

```
>>> kalc root2*5
7.07

>>> kalc percent(12,100000,30,360)
1 000.00
```

In source code of kalc module (kalc\src\kalc\plugins) there will be some examples of plugins files

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)