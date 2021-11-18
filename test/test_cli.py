import pytest
from click.testing import CliRunner
from kalc import cli
import pyperclip


def test_kalc_2_plus_2():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "2+2")
    assert result.output == "4.00\n"


def test_kalc_2_multiply_2():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "2*2")
    assert result.output == "4.00\n"


def test_kalc_sqrt_121():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "sqrt(121)")
    assert result.output == "11.00\n"


def test_kalc_55_minus_5_equal():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "55-5=")
    assert result.output == "55-5=50.00\n"


def test_kalc_1mln_divide_3_userfriendly_output():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "1000000/3 -uf")
    assert result.output == "333 333.33\n"


def test_kalc_expression_with_spaces():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "'3**2 + sin(pi/2) / exp(2)'")
    assert result.output == "9.14\n"


def test_kalc_10_exponentiation_8_round_to_5_decimal():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "10**8 -d 5")
    assert result.output == "100 000 000.00000\n"


def test_kalc_1mln_divide_3_without_decimal():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "1000000/3 -d 0 ")
    assert result.output == "333 333\n"


def test_kalc_clipboard():
    runner = CliRunner()
    runner.invoke(cli.kalc, "2*2 -c")
    clipboard_result = pyperclip.paste()
    assert clipboard_result == "4"


def test_kalc_sin_pi_divide_2():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "sin(pi/2)")
    assert result.output == "1.00\n"


def test_kalc_log_e():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "log(e)")
    assert result.output == "1.00\n"


def test_kalc_fsum_1_to_10():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "fsum([1,2,3,4,5,6,7,8,9,10])")
    assert result.output == "55.00\n"


def test_kalc_degrees_pi():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "degrees(pi)")
    assert result.output == "180.00\n"


def test_kalc_radians_180():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "radians(180) -d 10")
    assert result.output == "3.1415926536\n"


def test_kalc_pow_2_10():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "pow(2,10)")
    assert result.output == "1 024.00\n"


def test_kalc_floor_division_5_2():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "5//2")
    assert result.output == "2.00\n"


def test_kalc_modulus_5_2():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "5%2")
    assert result.output == "1.00\n"


def test_kalc_AttributeError():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "sinc(pi/2)")
    assert result.output == "NameError: name 'sinc' is not defined"


def test_kalc_SyntaxError():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "2:2")
    assert result.output == "SyntaxError: 2:2. Check operators"


def test_kalc_bool_eq():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "5==5")
    assert result.output == "1.00\n"


def test_kalc_bool_not_eq():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "5!=4")
    assert result.output == "1.00\n"


def test_kalc_bool_noq_more_eq():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "6>=5")
    assert result.output == "1.00\n"


def test_kalc_bool_noq_less_eq():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "4<=5")
    assert result.output == "1.00\n"


def test_kalc_bool_eq_expression():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "2+2==2*2")
    assert result.output == "1.00\n"


def test_kalc_bool_false_noq_more_eq():
    runner = CliRunner()
    result = runner.invoke(cli.kalc, "4>=5")
    assert result.output == "0.00\n"
