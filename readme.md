# Kalc

[![Python 3.6+](docs/resources/images/Python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)

[![Windows](docs/resources/images/os-windows-green.svg)](https://github.com/Rygor83/kalc) [![Linux](docs/resources/images/os-linux-green.svg)](https://github.com/Rygor83/kalc)

[![GitHub license](docs/resources/images/license-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Windows/Linux Command line calculator. Allows making calculations of any complexity directly in the console. Expandable
via plugins.

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

## Manual

[Kalc's manual](https://rygor83.github.io/kalc/)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)