#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

""" Evaluates the specified math expression """

import math
import os.path
import re
import logging
from pathlib import Path
import click
import click_log
import pyperclip
from yapsy.PluginManager import PluginManager
from yapsy.AutoInstallPluginManager import AutoInstallPluginManager
from yapsy.FilteredPluginManager import FilteredPluginManager
from yapsy.IPluginLocator import IPluginLocator
from yapsy.PluginFileLocator import PluginFileLocator, PluginFileAnalyzerWithInfoFile
from kalc.config import Config, KalcConfig
from kalc import __version__, PLUGIN_EXTENSION
from pprint import pformat
from collections import namedtuple

# Message color
color_message = {'bg': 'black', 'fg': 'white'}
color_success = {'bg': 'black', 'fg': 'green'}
color_warning = {'bg': 'black', 'fg': 'yellow'}
color_sensitive = {'bg': 'red', 'fg': 'white'}

Plugin_ref = namedtuple('Plugin', ['plugin_function_reference', 'string_function_reference', 'plugin_name',
                                   'plugin_class_reference'])
Plugin_ref.__new__.__defaults__ = (None, None, None, None)


def python_float_formater(val: str) -> str:
    """
    Convert string with numbers (int, float) in different formats (11.984,01; 11,984.01; 11984,01; 11984.01) into
    string with float in python format

    :param val: String with numbers (int, float) in different formats
    :return: String with float numbers in python formats
    """

    # TODO: check this examples - they are not correct. And write tests
    #   @Rygor ❯ kalc 1.000.000.000.000.000.000*2 -ff
    #   2 000 000 000 000 000.00
    #   @Rygor ❯ kalc 1.000.000.000.000.000.000*2 -ff
    #   2 000 000 000 000 000.00
    #   @Rygor ❯ kalc 1.000.000.000.000.000,000*2 -ff
    #   2 000 000 000 000 000.00
    #   @Rygor ❯ kalc 1,000,000,000,000,000.000*2 -ff
    #   2 000 000 000 000 000.00
    #   @Rygor ❯ kalc 1.000.000.000.000.000,000*2 -ff
    #   2 000 000 000 000 000.00
    #   @Rygor ❯ kalc 1,000,000,000,000,000,000*2 -ff
    #   2 000 000 000 000 000.00
    value = re.split(r"\.|,", val.strip())
    if len(value) > 1:
        newVal = str("".join(value[:-1]) + "." + value[-1])
    else:
        newVal = str("".join(value))
    return newVal


def function_help(ctx, param, value):
    """ Help on avaialable functions (math module and plugins)"""
    if not value or ctx.resilient_parsing:
        return

    cfg = Config()
    plugin_dirs = [str(Path(__file__).resolve().parent / 'plugins'), cfg.plugin_path]
    plug_func = load_plugins(plugin_dirs, type='dict')

    math_func = {item: f"math.{item}" for item in dir(math) if not item.startswith("__") and not item.endswith("__")}

    if str(value).lower() == 'list':
        click.echo(click.style('\nList of available functions', **color_success))
        click.echo(click.style('1. Plugins:', **color_success))
        click.echo(list(plug_func.keys()))
        click.echo(click.style('2. Math module:', **color_success))
        click.echo(list(math_func.keys()))
    elif value in plug_func:
        function_description = getattr(plug_func[value][0], '__doc__')
        click.echo(function_description)
    elif value in math_func:
        math_function_reference = getattr(math, value)
        function_description = getattr(math_function_reference, '__doc__')
        click.echo(function_description)
    else:
        click.echo(f"Function {str(value).upper()} is not available")

    ctx.exit()


def open_config(ctx, param, value):
    """
    Open configuration file for editing
    """
    if not value or ctx.resilient_parsing:
        return
    cfg = Config()
    cfg.open_config()
    ctx.exit()


def open_user_folder(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.launch(click.get_app_dir('kalc', roaming=False))
    ctx.exit()


def load_plugins(plugins_dirs: list, type: str):
    manager = PluginManager()
    pluglocator = PluginFileLocator()
    pluglocator.setPluginPlaces(plugins_dirs)
    analyzer = PluginFileAnalyzerWithInfoFile("kalc", (PLUGIN_EXTENSION))
    pluglocator.appendAnalyzer(analyzer)
    manager.setPluginLocator(pluglocator)
    manager.collectPlugins()

    plugin_functions_as_dict = {}
    plugin_functions_as_list = []

    for plugin in manager.getAllPlugins():
        for item in dir(plugin.plugin_object):
            if not item.startswith("__") and not item.endswith("__") and 'activate' not in item:
                if type == 'dict':
                    plugin_function_reference = getattr(plugin.plugin_object, item)
                    var_name = plugin.name.replace(" ", "_")
                    plugin_functions_as_dict[item] = Plugin_ref(plugin_function_reference,
                                                                f"{var_name}.plugin_object.{item}",
                                                                var_name, plugin)
                elif type == 'list':
                    plugin_functions_as_list.append(item)
                else:
                    pass
    plugin_functions = plugin_functions_as_dict if plugin_functions_as_dict else plugin_functions_as_list
    return plugin_functions


def plugins_install(ctx, param, value):
    """ Install plugins into plugins folder"""

    if not value or ctx.resilient_parsing:
        return

    existing_plugin_functions = {}
    cfg = Config()

    # Name conflict check
    captured_names_confilct = []

    plugin_dirs = [cfg.plugin_path, str(Path(__file__).resolve().parent / 'plugins')]
    existing_plugin_functions = load_plugins(plugin_dirs, type='dict')  # Load existing plugins

    logger.info(f"\nEXISING PLUGIN FUNCTIONS:")
    logger.info(pformat(existing_plugin_functions))

    math_functions = [item for item in dir(math) if not item.startswith("__") and not item.endswith("__")]
    logger.info(f"\nMATH MODULE FUNCTIONS:")
    logger.info(pformat(math_functions))

    new_plugin_dir = [str(Path(value).resolve().parent)]
    new_plug_func = load_plugins(new_plugin_dir, type='list')  # Load new plugins

    logger.info(f"\nNEW PLUGIN FUNCTIONS:")
    logger.info(pformat(new_plug_func))

    for new_item in new_plug_func:
        if new_item in existing_plugin_functions.keys():
            captured_names_confilct.append(
                (new_item, existing_plugin_functions[new_item].plugin_name,
                 existing_plugin_functions[new_item].plugin_class_reference.path))

    for new_item in new_plug_func:
        if new_item in math_functions:
            captured_names_confilct.append((new_item, 'MATH', ''))

    if captured_names_confilct:
        click.echo(
            click.style(
                f"\nFunction names conflict between new plugin and existing plugins/math module",
                **color_sensitive))
        for ind, item in enumerate(captured_names_confilct, start=1):
            click.echo(
                f"{ind}. Function name '{str(item[0]).upper()}' already exists in plugin/module '{item[1]}' \n  {item[2]}")
        click.echo("\nPlease rename you functions")
    # ---------------------------------------------------------------------------------------------------------------
    else:
        # Installation
        autoinstall = AutoInstallPluginManager(plugin_install_dir=cfg.plugin_path, plugin_info_ext=PLUGIN_EXTENSION)
        folder, file = os.path.split(value)
        result = autoinstall.install(directory=folder, plugin_info_filename=file)
        if result:
            print(f'Plugin is installed into "{cfg.plugin_path}" folder.')
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
@click.option("-d", "--decimal", "decimalplaces", help="Round a result up to <decimal> places",
              type=click.INT)
@click.option("-ff", "--free_format", "free_format",
              help="Enter float numbers in any format (11.984,01; 11,984.01; 11984,01; 11984.01)", is_flag=True,
              default=False)
@click.option("-function", help="Available functions help", callback=function_help, expose_value=False,
              is_eager=True, metavar="LIST / FUNCTION NAME")
@click.option("-config", is_flag=True, help="Open config", callback=open_config, expose_value=False, is_eager=True)
@click.option("-install", "--plugin_install", help="Install plugins into plugins folder", callback=plugins_install,
              expose_value=False, is_eager=True, metavar='<PATH TO *.KALC FILE>', type=click.Path())
@click.option("-user", is_flag=True, help="Open user folder", callback=open_user_folder, expose_value=False,
              is_eager=True)
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
    plugin_functions: dict = {}

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

    plugin_dirs = [cfg.plugin_path, str(Path(__file__).resolve().parent / 'plugins')]
    plugin_functions = load_plugins(plugin_dirs, type='dict')

    # ------------------------------------------------------------------------------------
    # Correct access to plugin module operators ( not func(), but <plugin_name>.plugin_object.func() ).
    # Replace only on word boundaries
    # ------------------------------------------------------------------------------------
    if plugin_functions:
        for function2substitute, value in plugin_functions.items():
            # Create new variable with plugin reference while eval()
            locals()[f"{value.plugin_name}"] = value.plugin_class_reference
            # Substitute
            expression = re.sub(rf"\b{function2substitute}\b", value.string_function_reference, expression)
        logger.info(f"Plugins call normalization: {expression}")

    # ------------------------------------------------------------------------------------
    # Correct access to MATH module operators ( not sqrt(), but math.sqrt() ). Replace only on word boundaries
    # ------------------------------------------------------------------------------------
    math_functions = {item: f"math.{item}" for item in dir(math) if
                      not item.startswith("__") and not item.endswith("__")}
    for function2substitute, value in math_functions.items():
        expression = re.sub(rf"\b{function2substitute}\b", value, expression)
    logger.info(f"Math module call normalization: {expression}")

    # ------------------------------------------------------------------------------------
    # Calculations
    # ------------------------------------------------------------------------------------
    # https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
    # Use eval() instead of ast.literal_eval() if the input is trusted (which it is in your case).
    # ------------------------------------------------------------------------------------
    ### Possible use or ast module instead of ast.literal_eval which can fail with ValueError: malformed node or string
    # import ast
    # tree = ast.parse(expression, mode='eval')
    # clause = compile(tree, '<AST>', 'eval')
    # result = eval(clause)
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
    # Substitute answer after comparison operators: True/False instead 1/0
    # ------------------------------------------------------------------------------------
    pattern = re.compile('[\w\s]([=!]=|[<>]=?)[\w\s]')  # searching for comparison operators
    if re.search(pattern, expression):
        pattern = re.compile('^0(\.?)(0*)$')  # searching for 0, 0.0, 0.00, 0.000 etc result
        if re.search(pattern, result):
            result = 'False'
        else:
            result = 'True'

    # ------------------------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------------------------
    output = f"{output}{result}"
    click.echo(output, nl=True)


if __name__ == "__main__":
    kalc()
