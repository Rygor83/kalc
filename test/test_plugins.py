"""
Test for plugin installation
Not a perfect test because left a working functionality rather than a refinement of a function for an external configuration file
But nevertheless test works
"""

import os
from click.testing import CliRunner
import pytest
from kalc import cli
from kalc.config import Config

# --------------------------------------- PLUGINS INSTALLATION ---------------------------------------

KALC_FILE_NAME = 'test_plugin.kalc'
PY_FILE_NAME = 'test_plugin.py'


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def conf():
    cfg = Config()
    cfg.create()
    yield cfg


@pytest.fixture
def plugins(tmp_path, conf):
    path_py_file = os.path.join(tmp_path, PY_FILE_NAME)
    path_kalc_file = os.path.join(tmp_path, KALC_FILE_NAME)
    installed_py_file = os.path.join(conf.plugin_path, PY_FILE_NAME)
    installed_kalc_file = os.path.join(conf.plugin_path, KALC_FILE_NAME)

    with open(path_py_file, 'w', encoding='utf-8') as file:
        file.write("from yapsy.IPlugin import IPlugin\n")
        file.write("class TestTest(IPlugin):\n")
        file.write("    def test01(self, percent, base_amount, days_in_month, days_in_year):\n")
        file.write("       return base_amount * percent * days_in_month / days_in_year / 100\n")
        file.write("    def test02(self, amount):\n")
        file.write("       return amount ** 2\n")

    with open(path_kalc_file, 'w', encoding='utf-8') as file:
        file.write("[Core]\n")
        file.write("Name = Plugin 1\n")
        file.write("Module = test_plugin\n")
        file.write("[Documentation]\n")
        file.write("Author = Rygor\n")
        file.write("Version = 0.1\n")
        file.write("Website = http: // rygor.by\n")
        file.write("Description = Example\n")

    yield path_py_file, path_kalc_file
    os.remove(path_py_file)
    os.remove(path_kalc_file)
    os.remove(installed_py_file)
    os.remove(installed_kalc_file)


def test_install_plugins(tmp_path, runner, conf, plugins):
    plugin_file = os.path.join(tmp_path, KALC_FILE_NAME)
    result = runner.invoke(cli.kalc, f"-install '{plugin_file}'")
    assert result.output == f'Plugin is installed into "{conf.plugin_path}" folder.\n'


# --------------------------------------- PLUGINS HELP ---------------------------------------
def test_help_list(runner):
    result = runner.invoke(cli.kalc, "--function list")
    assert result.output == '\nList of available functions\n1. Plugins:\nFunctions: compound_interest, sinterest\nConstants: root2\n2. Math module:\nFunctions: acos, acosh, asin, asinh, atan, atan2, atanh, ceil, comb, copysign, cos, cosh, degrees, dist, erf, erfc, exp, expm1, fabs, factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, isclose, isfinite, isinf, isnan, isqrt, lcm, ldexp, lgamma, log, log10, log1p, log2, modf, nextafter, perm, pow, prod, radians, remainder, sin, sinh, sqrt, tan, tanh, trunc, ulp\nConstants: e, inf, nan, pi, tau\n'


def test_help_plugin_sinterest(runner):
    result = runner.invoke(cli.kalc, "--function sinterest")
    assert result.output == '\n        Simple interest is a method to calculate the amount of interest charged on a principal amount at a given rate of interest and for a given period of time\n\n        :param percent: Rate of interest, for example 12\n        :param base_amount: Principal amount, for example 1000000\n        :param days_in_month: Days in given period of time, for example: 1 month = 30 days\n        :param days_in_year: Days in year, for example, 360/365/366\n        :return: Maturity amount\n\n        https://www.cuemath.com/commercial-math/simple-interest/\n        \n'


def test_help_plugin_const_root2(runner):
    result = runner.invoke(cli.kalc, "--function root2")
    assert result.output == 'root2 = 1.4142135623730951\n'


def test_help_math_sqrt(runner):
    result = runner.invoke(cli.kalc, "-f sqrt")
    assert result.output == 'Return the square root of x.\n'


def test_help_math_factorial(runner):
    result = runner.invoke(cli.kalc, "-f factorial")
    assert result.output == 'Find x!.\n\nRaise a ValueError if x is negative or non-integral.\n'


def test_help_math_const_pi(runner):
    result = runner.invoke(cli.kalc, "-f pi")
    assert result.output == 'pi = 3.141592653589793\n'


def test_help_math_const_e(runner):
    result = runner.invoke(cli.kalc, "-f e")
    assert result.output == 'e = 2.718281828459045\n'


# --------------------------------------- HELP WRONG FUNCTION ---------------------------------------

def test_wrong_command_xxxxx(runner):
    result = runner.invoke(cli.kalc, "-f xxxxx")
    assert str(result.output).strip() == "Function XXXXX is not available"
