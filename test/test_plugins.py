import pytest
from click.testing import CliRunner
from kalc import cli
import pyperclip


@pytest.fixture
def runner():
    return CliRunner()
