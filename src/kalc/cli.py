#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

import click
import math
import re
import pyperclip


@click.command()
@click.argument('expression')
@click.option('-u', '--userfriendly', 'userfriendly', help='Выводить с разделителями тысяч', is_flag=True,
              type=click.BOOL)
@click.option('-b', '--copytoclipboard', 'copytoclipboard', help='Копировать ответ в буфер обмена', is_flag=True,
              type=click.BOOL)
def kalc(expression, userfriendly=False, copytoclipboard=False):
    """ Вычисляет заданное выражение """

    # Замена некоторых операторов, которые есть в жизни, но в python они другие.
    expression = expression.replace(':', '/')

    # Замена операторов модуля math
    math_func = {item: f'math.{item}' for item in dir(math)}
    pattern = re.compile("|".join(math_func.keys()))
    expression = pattern.sub(lambda m: math_func[re.escape(m.group(0))], expression)
    print(expression)

    result = eval(str(expression))

    if copytoclipboard:
        pyperclip.copy(result)

    if userfriendly:
        print("{:,.2f}".format(result).replace(",", " "))
    else:
        print(result)


if __name__ == '__main__':
    kalc()
