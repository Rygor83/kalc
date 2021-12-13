#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

""" Evaluates the specified math expression """

import math
import re
import click
import pyperclip
from kalc.config import Config, KalcConfig


# TODO: используя Yapsy (https://pypi.org/project/Yapsy/) реалзовать систему плагинов, чтобы можно было писать
#  свои функции.


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


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("expression")
@click.option(
    "-uf",
    "--userfriendly",
    "userfriendly",
    help="User-friendly output. Separate thousands with a spaces",
    is_flag=True,
    type=click.BOOL,
)
@click.option(
    "-c",
    "--copytoclipboard",
    "copytoclipboard",
    help="Copy results into clipboard",
    is_flag=True,
    type=click.BOOL,
)
@click.option(
    "-d",
    "--rounddecimal",
    "rounddecimal",
    help="Round a result up to <rounddecimal> decimal",
    type=click.INT,
)
@click.option(
    "-config",
    is_flag=True,
    help="Open config",
    callback=open_config,
    expose_value=False,
    is_eager=True
)
def kalc(
        expression: str,
        userfriendly: bool = False,
        copytoclipboard: bool = False,
        rounddecimal: int = 0,
) -> None:
    """
    \b
    Evaluates the specified math EXPRESSION
    \b
    Usage: kalc <EXPRESSION>
    """

    output: str = ""

    _config: KalcConfig = Config().read()

    expression = expression.lower()

    # Preparing to display the entire expression and result i.e. 2+2=4
    pattern = re.compile('(=$|="$)')
    if re.search(pattern, expression):
        output = expression
        expression = re.sub(pattern, "", expression)

    # Convert all numbers to python float format
    expression = re.sub(r"\w((\d+|[.,])+)\w", lambda m: python_float_formater(m.group(0)), expression)

    # Correct access to math module operators ( not sqrt(), but math.sqrt() ). Replace only on word boundaries
    math_func = {item: f"math.{item}" for item in dir(math)}
    for key, value in math_func.items():
        expression = re.sub(rf"\b{key}\b", value, expression)

    # Calculations
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

    # Copy to clipboard ?!
    if any([copytoclipboard, _config.copytoclipboard]):
        pyperclip.copy(result)

    # Rounding
    if rounddecimal is not None:
        round_num = rounddecimal
    elif _config.decimalround:
        round_num = _config.decimalround
    else:
        round_num = 2

    # User-friendly output. Separate thousands with a spaces
    replace_symbol = " " if any([userfriendly, _config.userfriendly]) else ""
    result = f"{{:,.{round_num}f}}".format(result).replace(",", replace_symbol)

    # Output
    output = f"{output}{result}"
    click.echo(output, nl=True)


if __name__ == "__main__":
    kalc()
