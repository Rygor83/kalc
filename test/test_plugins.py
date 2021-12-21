import pytest
from click.testing import CliRunner
from kalc import cli
import pyperclip
from kalc.config import Config
import os


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def config(tmp_path):
    cfg = Config(config_path=tmp_path)
    cfg.create()
    yield cfg
    cfg.remove_config()
    cfg.remove_plugin_folder()


@pytest.fixture
def plugins(tmp_path):
    path_py_file = os.path.join(tmp_path, 'plg1.py')
    path_kalc_file = os.path.join(tmp_path, 'plg1.kalc')

    with open(path_py_file, 'w') as f:
        f.write("from yapsy.IPlugin import IPlugin\n")
        f.write("class PluginOne(IPlugin):\n")
        f.write("    def percent(self, percent, base_amount, days_in_month, days_in_year):\n")
        f.write("       return base_amount * percent * days_in_month / days_in_year / 100\n")
        f.write("    def double(self, amount):\n")
        f.write("       return amount ** 2\n")

    with open(path_kalc_file, 'w') as f:
        f.write("[Core]\n")
        f.write("Name = Plugin 1\n")
        f.write("Module = plg1\n")
        f.write("[Documentation]\n")
        f.write("Author = Rygor\n")
        f.write("Version = 0.1\n")
        f.write("Website = http: // rygor.by\n")
        f.write("Description = Example\n")

    yield path_py_file, path_kalc_file
    os.remove(path_py_file)
    os.remove(path_kalc_file)


def test_install_plugins(tmp_path, runner, config, plugins):
    plugin_file = os.path.join(tmp_path, 'plg1.kalc')
    config_file = os.path.join(tmp_path, 'kalc_config.ini')
    result = runner.invoke(cli.kalc, f"-install {plugin_file} -path {config_file}")
    assert result.output == f'Plugin "PLG1.KALC" is installed into "{config.plugin_path}" folder.'
