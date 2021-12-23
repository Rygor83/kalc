"""
Test for plugin installation
Not a perfect test because left a working functionality rather than a refinement of a function for an external configuration file
But nevertheless test works
"""

import pytest
from click.testing import CliRunner
from kalc import cli
import pyperclip
from kalc.config import Config
import os
from pathlib import Path

# --------------------------------------- PLUGINS INSTALLATION ---------------------------------------

kalc_file_name = 'test_plugin.kalc'
py_file_name = 'test_plugin.py'


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def config(tmp_path):
    cfg = Config()
    cfg.create()
    yield cfg


@pytest.fixture
def plugins(tmp_path, config):
    path_py_file = os.path.join(tmp_path, py_file_name)
    path_kalc_file = os.path.join(tmp_path, kalc_file_name)
    installed_py_file = os.path.join(config.plugin_path, py_file_name)
    installed_kalc_file = os.path.join(config.plugin_path, kalc_file_name)

    with open(path_py_file, 'w') as f:
        f.write("from yapsy.IPlugin import IPlugin\n")
        f.write("class TestTest(IPlugin):\n")
        f.write("    def test01(self, percent, base_amount, days_in_month, days_in_year):\n")
        f.write("       return base_amount * percent * days_in_month / days_in_year / 100\n")
        f.write("    def test02(self, amount):\n")
        f.write("       return amount ** 2\n")

    with open(path_kalc_file, 'w') as f:
        f.write("[Core]\n")
        f.write("Name = Plugin 1\n")
        f.write("Module = test_plugin\n")
        f.write("[Documentation]\n")
        f.write("Author = Rygor\n")
        f.write("Version = 0.1\n")
        f.write("Website = http: // rygor.by\n")
        f.write("Description = Example\n")

    yield path_py_file, path_kalc_file
    os.remove(path_py_file)
    os.remove(path_kalc_file)
    os.remove(installed_py_file)
    os.remove(installed_kalc_file)


def test_install_plugins(tmp_path, runner, config, plugins):
    plugin_file = os.path.join(tmp_path, kalc_file_name)
    result = runner.invoke(cli.kalc, f"-install '{plugin_file}'")
    assert result.output == f'Plugin is installed into "{config.plugin_path}" folder.\n'


# --------------------------------------- CORE PLUGINS HELP ---------------------------------------
def test_math_help_percent(runner):
    result = runner.invoke(cli.kalc, "-function percent")
    assert str(
        result.output).strip() == 'Returns maturity amount\n\n        :param percent: Rate of interest, 12\n        :param base_amount: Principal amount\n        :param days_in_month: Days in period\n        :param days_in_year: Days in year\n        :return: Maturity amount'


# --------------------------------------- MATH HELP ---------------------------------------
def test_math_help_sqrt(runner):
    result = runner.invoke(cli.kalc, "-function sqrt")
    assert str(result.output).strip() == 'Return the square root of x.'


def test_math_help_factorial(runner):
    result = runner.invoke(cli.kalc, "-function factorial")
    assert str(result.output).strip() == "Find x!.\n\nRaise a ValueError if x is negative or non-integral."


# --------------------------------------- HELP WRONG FUNCTION ---------------------------------------

def test_wrong_command_xxxxx(runner):
    result = runner.invoke(cli.kalc, "-function xxxxx")
    assert str(result.output).strip() == "Function XXXXX is not available"
