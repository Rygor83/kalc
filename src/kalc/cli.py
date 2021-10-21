#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------
import click
import math
import re
import pyperclip
import kalc.config as config


@click.command()
@click.argument('expression')
@click.option('-uf', '--userfriendly', 'userfriendly', help='User-friendly output. Separate thousands with a spaces',
              is_flag=True, type=click.BOOL)
@click.option('-c', '--copytoclipboard', 'copytoclipboard', help='Copy results into clipboard', is_flag=True,
              type=click.BOOL)
@click.option('-d', '--rounddecimal', 'rounddecimal', help='Round a result up to <rounddecimal> decimal',
              type=click.INT)
def kalc(expression, userfriendly=False, copytoclipboard=False, rounddecimal=0):
    """ Evaluates the specified math expression """

    output = ""

    _config = config.Config().read()

    expression = str(expression).lower()

    # Preparing to display the entire expression and result
    if "=" in expression:
        output = expression
        expression = expression.replace('=', '')

    # Correct access to math module operators ( not sqrt(), but math.sqrt() )
    math_func = {item: f'math.{item}' for item in dir(math)}
    pattern = re.compile("|".join(math_func.keys()))
    expression = pattern.sub(lambda m: math_func[re.escape(m.group(0))], expression)

    # Calculations
    result = eval(expression)

    # Copy to clipboard ?!
    if any([copytoclipboard, _config.copytoclipboard]):
        pyperclip.copy(result)

    # Rounding
    if rounddecimal:
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
    click.echo(output)


if __name__ == '__main__':
    kalc()
