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
@click.option('-uf', '--userfriendly', 'userfriendly', help='Выводить с разделителями тысяч', is_flag=True,
              type=click.BOOL)
@click.option('-b', '--copytoclipboard', 'copytoclipboard', help='Копировать ответ в буфер обмена', is_flag=True,
              type=click.BOOL)
@click.option('-r', '--rounddecimal', 'rounddecimal', help='Округлять десятичные знаки', type=click.INT)
def kalc(expression, userfriendly=False, copytoclipboard=False, rounddecimal=0):
    """ Вычисляет заданное выражение """
    output = ""

    _config = config.Config().read()

    if "=" in expression:
        output = expression
        expression = expression.replace('=', '')

    # Замена некоторых операторов, которые есть в жизни, но в python они другие.
    expression = expression.replace(':', '/')

    # Правильное обращение к операторам модуля math ( не sqrt(), а math.sqrt() )
    math_func = {item: f'math.{item}' for item in dir(math)}
    pattern = re.compile("|".join(math_func.keys()))
    expression = pattern.sub(lambda m: math_func[re.escape(m.group(0))], expression)

    result = eval(expression)

    # Копирование в буфер обмена
    if any([copytoclipboard, _config.copytoclipboard]):
        pyperclip.copy(result)

    # Округления
    if rounddecimal:
        round_num = rounddecimal
    elif _config.decimalround:
        round_num = _config.decimalround
    else:
        round_num = 2

    # Дружеский вывод с разделением на тысячи
    replace_symbol = " " if any([userfriendly, _config.userfriendly]) else ""

    result = f"{{:,.{round_num}f}}".format(result).replace(",", replace_symbol)

    output = f"{output}{result}"
    click.echo(output)

    if __name__ == '__main__':
        kalc()
