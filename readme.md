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
pip install <path to kalc folder>
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
  -config                         Open config file
  -ff, --free_format              Enter float numbers in any format (11.984,01; 11,984.01; 11984,01; 11984.01)
  -install, --plugin_install <PATH TO *.KALC FILE> 
                                  Install plugins into plugins folder
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
kalc "2 + 2 - 1"
kalc "fsum([1, 2, 3])"
```

- by default decimal part must be separated by dot (not comma). But if you use option -ff then decimal part can be in
  any format (11.984,01; 11,984.01; 11984,01; 11984.01)
```
kalc 11.984,01+11,984.01+11984,01+11984.01 -ff
>> 47 936.04
```
- expression must be written according to the common rules of writing math expression on a PC. For instance: x^2+sin(5*
  y)/exp(4*z)
- kalc module considers parenthesis ( i.e. '(' and ')' )
- kalc module knows the following operations:

| Operations                                                                                          | Description                             | Examples                        |
|:----------------------------------------------------------------------------------------------------|:----------------------------------------|:--------------------------------|
| **Basic operations**                                                                                |                                         |                                 |
| +                                                                                                   | addition                                | kalc 2+2 -> result 4            |
| -                                                                                                   | substraction                            | kalc 2-1 -> result 3            |
| /                                                                                                   | division                                | kalc 4/2 -> result 2            |
| *                                                                                                   | multiplication                          | kalc 3*3 -> result 9            |
| **                                                                                                  | exponentiation                          | kalc 3**2 -> result 9           |
| //                                                                                                  | floor division                          | kalc 6//4 -> result 1           |
| %                                                                                                   | modulus                                 | kalc 6%4 -> result 2            |
| **Functions**                                                                                       |                                         |                                 |
| sin                                                                                                 | sinus                                   | kalc sin(pi/2) -> result 1      |
| cos                                                                                                 | cosine                                  | kalc cos(pi)   -> result -1     |
| tan                                                                                                 | tangent                                 |                                 |
| exp                                                                                                 | exponent                                | kalc exp(2) -> result 7.39      |
| log                                                                                                 | natural logarithm                       | kalc log(e) -> result 1         |
| sqrt                                                                                                | square root                             | kalc sqrt(121) -> result 121    |
| trunc                                                                                               | truncation                              | kalc trunc(7.35) -> result 7    |
| Other functions from python [math](https://docs.python.org/3/library/math.html) module is available |                                         |                                 |
| **Numeric literals**                                                                                |                                         |                                 |
| pi                                                                                                  | The mathematical constant π = 3.141592… |                                 |
| e                                                                                                   | The mathematical constant e = 2.718281… |                                 |
| tau                                                                                                 | The mathematical constant τ = 6.283185… |                                 |
| **Comparison  Operators** Works only with quotes. Answers: True, False                  |                                         |                                 |
| ==                                                                                                  | equal                                   | "2==2" -> result 1.00 (True)    |
| !=                                                                                                  | not equal                               | "2!=2" -> result 0.00 (False)   |
| \>                                                                                                  | more                                    | "2>1" -> result 1.00 (True)     |
| <                                                                                                   | less                                    | "2<2" -> result 0.00 (False)    |
| > =                                                                                                 | more or equal                           | "2>=2" -> result 1.00 (True)    |
| <=                                                                                                  | less or equal                           | "2<=2" -> result 1.00 (True)    |

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
free_format      - Can use free format of float ((11.984,01; 11,984.01; 11984,01; 11984.01)). Values: True/False
                   **Side effects**: if you use free_format parameter from config file then use functions with multiple 
                   values carefully. For example FSUM([1,2,3,4,5,6,7,8,9,10]) will convert values 1,2,3,4,5,6,7,8,9,10
                   into 123456789.10. You have to delimite values with space and use quotes: 
                   "FSUM([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"  
```

Kalc's command options (-uf, -d, -c, -ff) have priority over configuration parameters.

## Plugins

You can extend kalc with plugins

You need to create 2 files in any place you like:
1. Plugin Info File Format with 'kalc' extension (for example, myplugin.kalc): 
   The plugin info file is a text file encoded in ASCII or UTF-8 and gathering, as its name suggests, some basic information about the plugin.
   * it gives crucial information needed to be able to load the plugin
   * it provides some documentation like information like the plugin author’s name and a short description fo the plugin functionality.
   
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
kalc -install <path to myplugin.kalc file>
>>> Plugin "MYPLUGIN.KALC" is installed into "c:\Users\USERNAME\AppData\Local\kalc\plugins" folder - for windows
>>> Plugin "MYPLUGIN.KALC" is installed into "/home/USERNAME/.local/share/kalc" folder - for Linux
```

Now you can use new functions and constants from plugin:
```
kalc root2*5
>>> 7.07

kalc percent(12,100000,30,360)
>>> 1 000.00

```

In source code of kalc module (kalc\src\kalc\plugins) there will be some examples of plugins files

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)