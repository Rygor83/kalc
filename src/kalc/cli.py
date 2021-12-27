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
import ast, operator
import types
import builtins

# Message color
color_message = {'bg': 'black', 'fg': 'white'}
color_success = {'bg': 'black', 'fg': 'green'}
color_warning = {'bg': 'black', 'fg': 'yellow'}
color_sensitive = {'bg': 'red', 'fg': 'white'}

Plugin_ref = namedtuple('Plugin', ['plugin_function_reference', 'string_function_reference', 'plugin_name',
                                   'plugin_class_reference'])
Plugin_ref.__new__.__defaults__ = (None, None, None, None)


def _safe_eval(node, variables, functions):
    """
    https://pretagteam.com/question/evaluate-math-equations-from-unsafe-user-input-in-python

    :param node:
    :param variables:
    :param functions:
    :return:
    """
    _operations = {
        # Math
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        # Compare
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.GtE: operator.ge,
        ast.Gt: operator.gt,
        ast.LtE: operator.le,
        ast.Lt: operator.lt,
        # Bool
        ast.And: operator.and_,
        ast.Or: operator.or_,
        # Structures
        ast.List: list,
        ast.Dict: dict,
        ast.Set: set,
        # Bitwise
        ast.BitOr: operator.or_,
        ast.BitAnd: operator.and_,
        ast.BitXor: operator.xor,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        # Unary
        ast.Invert: operator.invert,
        ast.Not: operator.not_,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Name):
        return variables[node.id]  # KeyError -> Unsafe variable
    elif isinstance(node, ast.BinOp):
        op = _operations[node.op.__class__]  # KeyError -> Unsafe operation
        left = _safe_eval(node.left, variables, functions)
        right = _safe_eval(node.right, variables, functions)
        if isinstance(node.op, ast.Pow):
            assert right < 10000, f"Power must be less then 100. You use {right}"
        return op(left, right)
    elif isinstance(node, ast.Compare):
        op = _operations[node.ops[0].__class__]  # KeyError -> Unsafe operation
        left = _safe_eval(node.left, variables, functions)
        right = _safe_eval(node.comparators[0], variables, functions)
        return op(left, right)
    elif isinstance(node, ast.BoolOp):
        op = _operations[node.op.__class__]  # KeyError -> Unsafe operation
        left = _safe_eval(node.values[0], variables, functions)
        right = _safe_eval(node.values[1], variables, functions)
        return op(left, right)
    elif isinstance(node, ast.UnaryOp):
        op = _operations[node.op.__class__]  # KeyError -> Unsafe operation
        left = _safe_eval(node.operand, variables, functions)
        return op(left)
    elif isinstance(node, ast.List):
        op = _operations[node.__class__]  # KeyError -> Unsafe operation
        left = [arg.value for arg in node.elts]
        return op(left)
    elif isinstance(node, ast.Call):
        assert not node.keywords
        assert isinstance(node.func, ast.Name), f"Unsafe function derivation '{node.func.attr}'"
        func = functions[node.func.id]  # KeyError -> Unsafe function
        args = [_safe_eval(arg, variables, functions) for arg in node.args]
        return func(*args)

    assert False, 'Unsafe operation'


def safe_eval(expr, variables={}, functions={}):
    node = ast.parse(expr, '<string>', 'eval').body

    logger.info(ast.dump(node))

    return _safe_eval(node, variables, functions)


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

    # 1000000.00 - yes, 1 dot
    # 1000000,00 - yes, 1 comma
    # 1.000.000,00 - yes, several dots and 1 comma
    # 1,000,000.00 - yes, 1 dot and several commas
    #
    # 1000000 - no, no dot and no comma
    # 1.000.000 - no, several dots
    # 1,000,000 - no, several commas
    #
    # 1.000 - don't know
    # 1,000 - don't know

    value = re.split(r"\.|,", val.strip())
    if len(value) > 1:
        newVal = str("".join(value[:-1]) + "." + value[-1])
    else:
        newVal = str("".join(value))
    return newVal


def load_python_modules():
    math_functions = {item: getattr(math, f"{item}") for item in dir(math) if
                      not item.startswith("__") and not item.endswith("__") and type(
                          getattr(math, f"{item}")) == types.BuiltinFunctionType}
    math_constants = {item: getattr(math, f"{item}") for item in dir(math) if
                      not item.startswith("__") and not item.endswith("__") and type(
                          getattr(math, f"{item}")) == float}
    return math_functions, math_constants


def function_help(ctx, param, value):
    """ Help on avaialable functions (math module and plugins)"""
    if not value or ctx.resilient_parsing:
        return

    cfg = Config()
    plugin_dirs = [str(Path(__file__).resolve().parent / 'plugins'), cfg.plugin_path]
    plug_func, plug_const = load_plugins(plugin_dirs)

    # math_func = {item: f"math.{item}" for item in dir(math) if not item.startswith("__") and not item.endswith("__")}

    math_func, math_cons = load_python_modules()

    if str(value).lower() == 'list':
        click.echo(click.style('\nList of available functions', **color_success))
        click.echo(click.style('1. Plugins:', **color_success))
        click.echo(f"{click.style('Functions:', **color_warning)} {', '.join(list(plug_func.keys()))}")
        click.echo(f"{click.style('Constants', **color_warning)}: {', '.join(list(plug_const.keys()))}")
        click.echo(click.style('2. Math module:', **color_success))
        click.echo(f"{click.style('Functions', **color_warning)}: {', '.join(list(math_func.keys()))}")
        click.echo(f"{click.style('Constants', **color_warning)}: {', '.join(list(math_cons.keys()))}")
    elif value in plug_func:
        function_description = getattr(plug_func[value], '__doc__')
        click.echo(function_description)
    elif value in plug_const:
        click.echo(f"{value} = {plug_const[value]}")
    elif value in math_func:
        function_description = getattr(getattr(math, value), '__doc__')
        click.echo(function_description)
    elif value in math_cons:
        function_description = getattr(math, value)
        click.echo(f"{value} = {function_description}")
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


def load_plugins(plugins_dirs: list):
    manager = PluginManager()
    pluglocator = PluginFileLocator()
    pluglocator.setPluginPlaces(plugins_dirs)
    analyzer = PluginFileAnalyzerWithInfoFile("kalc", (PLUGIN_EXTENSION))
    pluglocator.appendAnalyzer(analyzer)
    manager.setPluginLocator(pluglocator)
    manager.collectPlugins()

    plugin_functions = {}
    plugin_constants = {}

    for plugin in manager.getAllPlugins():
        for item in dir(plugin.plugin_object):
            if not item.startswith("__") and not item.endswith("__") and 'activate' not in item:
                if isinstance(getattr(plugin.plugin_object, item), types.MethodType):
                    plugin_functions[item] = getattr(plugin.plugin_object, item)
                elif not isinstance(getattr(plugin.plugin_object, item), types.MethodType):
                    plugin_constants[item] = getattr(plugin.plugin_object, item)

    return plugin_functions, plugin_constants


def plugins_install(ctx, param, value):
    """ Install plugins into plugins folder"""

    if not value or ctx.resilient_parsing:
        return

    existing_plugin_functions = {}
    existing_plugin_constants = {}
    math_functions = {}
    math_constants = {}
    captured_names_confilct = []

    cfg = Config()

    plugin_dirs = [cfg.plugin_path, str(Path(__file__).resolve().parent / 'plugins')]
    existing_plugin_functions, existing_plugin_constants = load_plugins(plugin_dirs)  # Load existing plugins

    logger.info(f"\nEXISING PLUGIN FUNCTIONS AND CONSTANTS:")
    logger.info(list(existing_plugin_functions.keys()))
    logger.info(list(existing_plugin_constants.keys()))

    math_functions, math_constants = load_python_modules()
    logger.info(f"\nMATH MODULE FUNCTIONS AND CONSTANTS:")
    logger.info(list(math_functions.keys()))
    logger.info(list(math_constants.keys()))

    new_plugin_dir = [str(Path(value).resolve().parent)]
    new_plug_func, new_plug_const = load_plugins(new_plugin_dir)  # Load new plugins

    logger.info(f"\nNEW PLUGIN FUNCTIONS:")
    logger.info(list(new_plug_func.keys()))
    logger.info(list(new_plug_const.keys()))

    for new_item in new_plug_func:
        if new_item in existing_plugin_functions.keys():
            # TODO: указать про какой модуль разговор
            captured_names_confilct.append(
                (new_item, "", ""))

    for new_item in new_plug_func:
        if new_item in math_functions.keys():
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
            click.echo(f'Plugin is installed into "{cfg.plugin_path}" folder.')
        else:
            click.echo(f'Failed to install "{file.upper()}".')

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
@click.option("-f", "--function", help="Available functions help", callback=function_help, expose_value=False,
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
    plugin_functions, plugin_constants = load_plugins(plugin_dirs)

    # ------------------------------------------------------------------------------------
    # Correct access to MATH module operators ( not sqrt(), but math.sqrt() ). Replace only on word boundaries
    # ------------------------------------------------------------------------------------
    math_functions, math_constants = load_python_modules()

    # ------------------------------------------------------------------------------------

    allowed_functions = {**math_functions, **plugin_functions}
    allowed_constants = {**math_constants, **plugin_constants}

    # ------------------------------------------------------------------------------------
    # Calculations
    # ------------------------------------------------------------------------------------

    try:
        result = safe_eval(expression, allowed_constants, allowed_functions)
    except AttributeError as err:
        logger.error(err)
        raise SystemExit from err
    except SyntaxError as err:
        logger.error(f"SyntaxError: {err.args[1][3]}. Check the operators used")
        raise SystemExit from err
    except NameError as err:
        logger.error(err)
        raise SystemExit from err
    except TypeError as err:
        logger.error(err)
        raise SystemExit from err
    except ZeroDivisionError as err:
        logger.error(err)
        raise SystemExit from err
    except AssertionError as err:
        logger.error(err)
        raise SystemExit from err
    except KeyError as err:
        logger.error(f"KeyError. Function {err} is not permited. Run 'kalc -function list' for permited functions")
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
        if type(result) == int:
            round_num = 0
        result = f"{result:,.{round_num}f}".replace(",", replace_symbol)
    except OverflowError as err:
        logger.error(f"NameError: {err.args[0]}")
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
