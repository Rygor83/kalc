""" Test for math operations """
import click
import pytest
import pyperclip
from click.testing import CliRunner
from kalc import cli
import os
from pathlib import Path


@pytest.fixture
def runner():
    return CliRunner()


# --------------------------------------- MATH OPERATIONS ---------------------------------------
def test_math_2_plus_2(runner):
    result = runner.invoke(cli.kalc, "2+2")
    assert result.output == "4\n"


def test_math_2_multiply_2(runner):
    result = runner.invoke(cli.kalc, "2*2")
    assert result.output == "4\n"


def test_math_55_minus_5_equal(runner):
    result = runner.invoke(cli.kalc, "55-5=")
    assert result.output == "55-5=50\n"


# --------------------------------------- KALC'S OPTIONS ---------------------------------------
def test_math_1mln_divide_3_userfriendly_true_output(runner):
    result = runner.invoke(cli.kalc, "1000000/3 -uf true")
    assert result.output == "333 333.33\n"


def test_math_1mln_divide_3_userfriendly_false_output(runner):
    result = runner.invoke(cli.kalc, "1000000/3 -uf false")
    assert result.output == "333333.33\n"


def test_math_expression_with_spaces(runner):
    result = runner.invoke(cli.kalc, "'3**2 + sin(pi/2) / exp(2)'")
    assert result.output == "9.14\n"


def test_kalc_10_1_exponentiation_8_round_to_5_decimal(runner):
    result = runner.invoke(cli.kalc, "10.1**8 -d 5")
    assert result.output == "108 285 670.56281\n"


def test_math_1mln_divide_3_without_decimal(runner):
    result = runner.invoke(cli.kalc, "1000000/3 -d 0 ")
    assert result.output == "333 333\n"


def test_math_clipboard(runner):
    runner.invoke(cli.kalc, "2*2 -c")
    clipboard_result = pyperclip.paste()
    assert clipboard_result == "4"


# --------------------------------------- FUNCTIONS ---------------------------------------
def test_math_sqrt_121(runner):
    result = runner.invoke(cli.kalc, "sqrt(121)")
    assert result.output == "11.00\n"


def test_math_sin_pi_divide_2(runner):
    result = runner.invoke(cli.kalc, "sin(pi/2)")
    assert result.output == "1.00\n"


def test_math_log_e(runner):
    result = runner.invoke(cli.kalc, "log(e)")
    assert result.output == "1.00\n"


def test_math_fsum_1_to_10(runner):
    result = runner.invoke(cli.kalc, "fsum([1,2,3,4,5,6,7,8,9,10])")
    assert result.output == "55.00\n"


def test_math_degrees_pi(runner):
    result = runner.invoke(cli.kalc, "degrees(pi)")
    assert result.output == "180.00\n"


def test_math_radians_180(runner):
    result = runner.invoke(cli.kalc, "radians(180) -d 10")
    assert result.output == "3.1415926536\n"


def test_math_pow_2_10(runner):
    result = runner.invoke(cli.kalc, "pow(2,10)")
    assert result.output == "1 024.00\n"


def test_math_floor_division_5_2(runner):
    result = runner.invoke(cli.kalc, "5//2")
    assert result.output == "2\n"


def test_math_modulus_5_2(runner):
    result = runner.invoke(cli.kalc, "5%2")
    assert result.output == "1\n"


def test_math_factorial(runner):
    result = runner.invoke(cli.kalc, "factorial(5)")
    assert result.output == "120\n"


# --------------------------------------- ERRORS ---------------------------------------
def test_kalc_attributeError(runner):
    result = runner.invoke(cli.kalc, "sinc(pi/2)")
    assert result.output == "error: KeyError. Function 'sinc' is not permited. Run 'kalc -function list' for permited functions\n"


def test_kalc_syntaxError(runner):
    result = runner.invoke(cli.kalc, "2:2")
    assert result.output == 'error: SyntaxError: 2:2. Check the operators used\n'


# --------------------------------------- COMPARISON ---------------------------------------
def test_comp_eq(runner):
    result = runner.invoke(cli.kalc, "5==5")
    assert result.output == "True\n"


def test_comp_eq_with_space(runner):
    result = runner.invoke(cli.kalc, "'5 == 5'")
    assert result.output == "True\n"


def test_comp_not_eq(runner):
    result = runner.invoke(cli.kalc, "5!=4")
    assert result.output == "True\n"


def test_comp_not_eq_with_space(runner):
    result = runner.invoke(cli.kalc, "'5 != 4'")
    assert result.output == "True\n"


def test_comp_noq_more_eq(runner):
    result = runner.invoke(cli.kalc, "6>=5")
    assert result.output == "True\n"


def test_comp_noq_more_eq_with_space(runner):
    result = runner.invoke(cli.kalc, "'6 >= 5'")
    assert result.output == "True\n"


def test_comp_noq_less_eq(runner):
    result = runner.invoke(cli.kalc, "4<=5")
    assert result.output == "True\n"


def test_comp_eq_expression(runner):
    result = runner.invoke(cli.kalc, "2+2==2*2")
    assert result.output == "True\n"


def test_comp_eq_expression_with_spaces(runner):
    result = runner.invoke(cli.kalc, "'2 + 2 == 2 * 2'")
    assert result.output == "True\n"


def test_comp_false_noq_more_eq(runner):
    result = runner.invoke(cli.kalc, "4>=5")
    assert result.output == "False\n"


# --------------------------------------- BOOL ---------------------------------------

def test_bool_and(runner):
    result = runner.invoke(cli.kalc, "'1 and 0'")
    assert result.output == "0\n"


def test_bool_or(runner):
    result = runner.invoke(cli.kalc, "'1 or 0'")
    assert result.output == "1\n"


def test_bool_not_1(runner):
    result = runner.invoke(cli.kalc, "'not 1'")
    assert result.output == "0.00\n"


def test_bool_not_0(runner):
    result = runner.invoke(cli.kalc, "'not 0'")
    assert result.output == "1.00\n"


# --------------------------------------- BITWISE ---------------------------------------
def test_bitwise_right_shift(runner):
    result = runner.invoke(cli.kalc, "'10 << 1'")
    assert result.output == '20\n'


def test_bitwise_left_shift(runner):
    result = runner.invoke(cli.kalc, "'10 >> 1'")
    assert result.output == '5\n'


def test_bitwise_and(runner):
    result = runner.invoke(cli.kalc, "'10 & 1'")
    assert result.output == '0\n'


def test_bitwise_or(runner):
    result = runner.invoke(cli.kalc, "'10 | 1'")
    assert result.output == '11\n'


def test_bitwise_not(runner):
    result = runner.invoke(cli.kalc, "'~10'")
    assert result.output == '-11\n'


def test_bitwise_xor(runner):
    result = runner.invoke(cli.kalc, "'10 ^ 1'")
    assert result.output == '11\n'


# --------------------------------------- FLOAT FREE FORMAT ---------------------------------------
def test_float_free_fromat_01(runner):
    result = runner.invoke(cli.kalc, "11.984,01*2 -ff")
    assert result.output == '23 968.02\n'


def test_float_free_fromat_02(runner):
    result = runner.invoke(cli.kalc, "11,984.01*2 -ff")
    assert result.output == '23 968.02\n'


def test_float_free_fromat_03(runner):
    result = runner.invoke(cli.kalc, "11984,01*2 -ff")
    assert result.output == '23 968.02\n'


def test_float_free_fromat_04(runner):
    result = runner.invoke(cli.kalc, "11984.01*2 -ff")
    assert result.output == '23 968.02\n'


def test_float_free_fromat_05(runner):
    result = runner.invoke(cli.kalc, "12.435,84*20/120 -ff")
    assert result.output == '2 072.64\n'


def test_float_free_format_06(runner):
    result = runner.invoke(cli.kalc, "'fsum([11.984,01, 11,984.01])' -ff")
    assert result.output == '23 968.02\n'


# --------------------------------------- CORE PLUGINS ---------------------------------------
def test_core_plugin_root2(runner):
    result = runner.invoke(cli.kalc, "root2**2")
    assert result.output == '2.00\n'


def test_core_plugin_percent(runner):
    result = runner.invoke(cli.kalc, "sinterest(12,1000000,30,360)")
    assert result.output == '10 000.00\n'


# --------------------------------------- ERROR CASES ---------------------------------------
def test_error_zerodivisionerror(runner):
    result = runner.invoke(cli.kalc, "1/0")
    assert result.output == 'error: division by zero\n'


def test_error_overflowerror(runner):
    result = runner.invoke(cli.kalc, "1000000000000000000000000000000**103")
    assert result.output == 'error: NameError: int too large to convert to float\n'


# --------------------------------------- UNSAFE OPERATIONS ---------------------------------------

def test_delete_folder(runner):
    result = runner.invoke(cli.kalc, "__import__('os').remove('file')")
    assert result.output == "error: Unsafe function derivation 'remove'\n"


# --------------------------------------- PROBLEMS ---------------------------------------
@pytest.mark.skip(
    reason="""This is problem with f-string in python 3.10 and 3.9. Calculations are done right, 
              but User-friendly output with f-string ruins the answer""")
def test_problem1(runner):
    result = runner.invoke(cli.kalc, "1000000000000**2")
    assert result.output == '1 000 000 000 000 000 000 000 000\n'


def test_kalc_1_000_000_000_000_000_000_x_2_free_format_01(runner):
    result = runner.invoke(cli.kalc, "1.000.000.000.000.000.000*2 -ff")
    assert result.output == "2 000 000 000 000 000 000.00\n"


def test_kalc_1_000_000_000_000_000_000_x_2_free_format_02(runner):
    result = runner.invoke(cli.kalc, "1,000,000,000,000,000,000*2 -ff")
    assert result.output == "2 000 000 000 000 000 000.00\n"


def test_kalc_1_000_000_000_000_000_000_x_2_free_format_03(runner):
    result = runner.invoke(cli.kalc, "1.000.000.000.000.000,000*2 -ff")
    assert result.output == "2 000 000 000 000 000.00\n"


def test_kalc_1_000_000_000_000_000_000_x_2_free_format_04(runner):
    result = runner.invoke(cli.kalc, "1,000,000,000,000,000.000*2 -ff")
    assert result.output == "2 000 000 000 000 000.00\n"
