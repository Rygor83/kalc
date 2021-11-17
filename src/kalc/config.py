#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------
""" Configuration file management """

import errno
import os
from configparser import ConfigParser
import pathlib
from typing import Union, NamedTuple
from appdirs import user_data_dir
import click


class KalcConfig(NamedTuple):
    """Object containing configuration's parameters"""

    decimalround: int
    copytoclipboard: bool
    userfriendly: bool


class Config:
    """Configuration file management"""

    def __init__(self):
        self.ini_name = "kalc_config.ini"
        self.config_path = os.path.join(self.set_path, self.ini_name)

    def read(self) -> KalcConfig:
        """Return KalcConfig object after reading configuration file"""
        parser = ConfigParser(interpolation=None)
        if not self.exists():
            self.create()

        parser.read(self.config_path)
        decimalround = parser.getint("GENERAL", "decimalround")
        copytoclipboard = parser.getboolean("GENERAL", "copytoclipboard")
        userfriendly = parser.getboolean("GENERAL", "userfriendly")

        return KalcConfig(decimalround, copytoclipboard, userfriendly)

    def create(self) -> None:
        """Creating a configuration file"""
        parser = ConfigParser()
        parser["GENERAL"] = {
            "decimalround": "Round a result up to <decimalround> decimal. Values: integer 1,2,3",
            "copytoclipboard": "Need to copy results into clipboard. Values: True/False",
            "userfriendly": "Need to separate thousands with a space. Values: True/False",
        }

        with open(self.config_path, "w+", encoding="utf-8") as configfile:
            parser.write(configfile)

        click.echo(f"Path to ini file: {click.format_filename(self.config_path)} \n")
        click.echo(click.style("INI file is created"))
        click.echo(
            click.style("!!! Fill in all the required parameters in the file !!! \n")
        )
        click.launch(self.config_path)
        click.pause()

    def exists(self) -> bool:
        """Checking if config file exists"""
        return os.path.exists(self.config_path)

    @property
    def set_path(self) -> Union[str, pathlib.Path]:
        """Setting path for saving config file"""
        path = user_data_dir("kalc", appauthor=False)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        return path

    def open_config(self) -> None:
        """Open configuration file for editing"""
        click.launch(self.config_path)
