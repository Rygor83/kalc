#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

""" Evaluates the specified math expression """

import math
import os.path
import re
import click
import click_log
import pyperclip
import logging
from yapsy.PluginManager import PluginManager
from yapsy.AutoInstallPluginManager import AutoInstallPluginManager
from yapsy.FilteredPluginManager import FilteredPluginManager
from kalc.config import Config, KalcConfig
from kalc import __version__, PLUGIN_EXTENSION
from pathlib import Path


def python_float_formater(val):
    """
    Convert string with numbers (int, float) in different formats (11.984,01; 11,984.01; 11984,01; 11984.01) into
    string with float in python format

    :param val: String with numbers (int, float) in different formats
    :return: String with float numbers in python formats
    """
    value = re.split(r"\.|,", val.strip())
    if len(value) > 1:
        newVal = str("".join(value[:-1]) + "." + value[-1])
    else:
        newVal = str("".join(value))
    return newVal


def open_config(ctx, param, value):
    """
    Open configuration file for editing
    """
    if not value or ctx.resilient_parsing:
        return
    cfg = Config()
    cfg.open_config()
    ctx.exit()


def plugins_install(ctx, param, value):
    """ Install plugins into plugins folder"""
    # TODO: Доделать инсталяцию плагинов

    if not value or ctx.resilient_parsing:
        return

    cfg = Config()

    autoinstall = AutoInstallPluginManager(plugin_install_dir=cfg.plugin_path, plugin_info_ext=PLUGIN_EXTENSION)
    folder, file = os.path.split(value)
    result = autoinstall.install(directory=folder, plugin_info_filename=file)
    if result:
        print(f'Plugin "{file.upper()}" is installed into "{cfg.plugin_path}" folder.')
    else:
        print(f'Failed to install "{file.upper()}".')
    ctx.exit()


logger = logging.getLogger(__name__)
click_log.basic_config(logger)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], token_normalize_func=lambda x: x.lower())
log_level = ['--log_level', '-l']


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("expression")
@click.option("-uf", "--userfriendly", "userfriendly", help="User-friendly output. Separate thousands with a spaces",
              type=click.BOOL, default=None)
@click.option("-c", "--copytoclipboard", "copytoclipboard", help="Copy results into clipboard", is_flag=True,
              type=click.BOOL)
@click.option("-d", "--decimal", "decimalplaces", help="Round a result up to <rounddecimal>",
              type=click.INT)
@click.option("-ff", "--free_format", "free_format",
              help="Enter float numbers in any format (11.984,01; 11,984.01; 11984,01; 11984.01)", is_flag=True,
              default=False)
@click.option("-config", is_flag=True, help="Open config", callback=open_config, expose_value=False, is_eager=True)
@click.option("-install", "--plugin_install", help="Install plugins into plugins folder", callback=plugins_install,
              expose_value=False, is_eager=True, metavar='<PATH TO *.KALC FILE>', type=click.Path())
@click.option('-path', '--config_path', 'config_path', help="Path to external sap_config.ini folder",
              type=click.Path(exists=True, dir_okay=True))
@click.version_option(version=__version__)
@click_log.simple_verbosity_option(logger, *log_level, default='ERROR')
@click.pass_context
def kalc(ctx, expression: str, userfriendly: bool, copytoclipboard: bool = False, decimalplaces: int = 0,
         free_format: bool = False, config_path: str = '', verbosity='INFO') -> None:
    """
    \b
    Evaluates the specified math EXPRESSION
    \b
    Usage: kalc <EXPRESSION>
    """

    output: str = ""
    plug_func: dict = {}

    cfg = Config(config_path)
    _config: KalcConfig = cfg.read()

    expression = expression.lower()
    logger.info(f"Initial expression: {expression}")

    # ------------------------------------------------------------------------------------
    # Preparing to display the entire expression and result i.e. 2+2=4
    # ------------------------------------------------------------------------------------
    pattern = re.compile('(=$|="$)')
    if re.search(pattern, expression):
        output = expression
    expression = re.sub(pattern, "", expression)

    # ------------------------------------------------------------------------------------
    # Convert all numbers to python float format
    # ------------------------------------------------------------------------------------
    if any([free_format, _config.free_format]):
        expression = re.sub(r"\w((\d+|[.,])+)\w", lambda m: python_float_formater(m.group(0)), expression)
        logger.info(f"Conversion to python float format: {expression}")

    # ------------------------------------------------------------------------------------
    # Load plugins
    # ------------------------------------------------------------------------------------

    lvl = logger.getEffectiveLevel()  # Get logging level from click_log
    logging.basicConfig(level=lvl)  # pass loggin level to yapsy logger
    logging.getLogger('yapsy').setLevel(lvl)

    manager = PluginManager()
    manager = FilteredPluginManager(manager)
    manager.isPluginOk = lambda x: x.description != ""  # Some day this may be helpfull, but not right now
    manager.setPluginInfoExtension(PLUGIN_EXTENSION)
    manager.setPluginPlaces([cfg.plugin_path, str(Path.cwd() / 'plugins')])
    manager.setPluginPlaces([cfg.plugin_path, str(Path(__file__).resolve().parent / 'plugins')])
    manager.collectPlugins()

    rejected_plug = manager.getRejectedPlugins()
    if rejected_plug:
        logger.info(f"Rejected plugins: {rejected_plug}")

    # ------------------------------------------------------------------------------------
    # Correct access to plugin module operators ( not func(), but plugin.plugin_object.func() ).
    # Replace only on word boundaries
    # ------------------------------------------------------------------------------------
    for plugin in manager.getAllPlugins():
        plug_func = {item: f"plugin.plugin_object.{item}" for item in dir(plugin.plugin_object) if
                     not item.startswith("__") and not item.endswith("__") and 'activate' not in item}

    if plug_func:
        for key, value in plug_func.items():
            expression = re.sub(rf"\b{key}\b", value, expression)
        logger.info(f"Plugins call normalization: {expression}")

        # ------------------------------------------------------------------------------------
        # Correct access to MATH module operators ( not sqrt(), but math.sqrt() ). Replace only on word boundaries
        # ------------------------------------------------------------------------------------
        math_func = {item: f"math.{item}" for item in dir(math)}
        for key, value in math_func.items():
            expression = re.sub(rf"\b{key}\b", value, expression)
        logger.info(f"Math module call normalization: {expression}")

    # ------------------------------------------------------------------------------------
    # Calculations
    # ------------------------------------------------------------------------------------

    try:
        result: str = eval(expression)
    except AttributeError as err:
        click.echo(f"AttributeError: {err}", nl=False)
        raise SystemExit from err
    except SyntaxError as err:
        click.echo(f"SyntaxError: {err.args[1][3]}. Check operators", nl=False)
        raise SystemExit from err
    except NameError as err:
        click.echo(f"NameError: {err.args[0]}", nl=False)
        raise SystemExit from err

    # TODO: попробовать заменять 1 и 0 в логическх операциях сравнения. Например, kalc "pi != e" выдает 1.00
    #   и вот вместо 1.00 возвращать True.

    # ------------------------------------------------------------------------------------
    # Copy to clipboard ?!
    # ------------------------------------------------------------------------------------
    if any([copytoclipboard, _config.copytoclipboard]):
        pyperclip.copy(result)

    # ------------------------------------------------------------------------------------
    # Rounding
    # ------------------------------------------------------------------------------------
    if decimalplaces is not None:
        round_num = decimalplaces
    elif _config.decimalplaces:
        round_num = _config.decimalplaces
    else:
        round_num = 2

    # ------------------------------------------------------------------------------------
    # User-friendly output. Separate thousands with a spaces
    # ------------------------------------------------------------------------------------
    if userfriendly is not None:
        replace_symbol = " " if userfriendly is True else ""
    elif _config.userfriendly:
        replace_symbol = " "
    else:
        replace_symbol = ""

    try:
        result = f"{{:,.{round_num}f}}".format(result).replace(",", replace_symbol)
    except OverflowError as err:
        click.echo(f"NameError: {err.args[0]}", nl=False)
        raise SystemExit from err

    # ------------------------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------------------------
    output = f"{output}{result}"
    click.echo(output, nl=True)


if __name__ == "__main__":
    kalc()
