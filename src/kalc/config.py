#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------
""" Configuration file management """

import errno
import os
from configparser import ConfigParser
import pathlib
from typing import Union, NamedTuple
import click
import shutil


class KalcConfig(NamedTuple):
    """Object containing configuration's parameters"""

    decimalplaces: int
    copytoclipboard: bool
    userfriendly: bool
    free_format: bool


class Config:
    """Configuration file management"""

    def __init__(self, config_path: Union[str, pathlib.Path] = None):
        self.ini_name = "kalc_config.ini"
        self.plugin_folder_name = "plugins"
        self.config_path = os.path.join(config_path, self.ini_name) if config_path else os.path.join(self.set_path,
                                                                                                     self.ini_name)
        self.plugin_path = os.path.join(config_path, 'plugins') if config_path else os.path.join(self.set_path,
                                                                                                 self.plugin_folder_name)

    def read(self) -> KalcConfig:
        """Return KalcConfig object after reading configuration file"""
        parser = ConfigParser(interpolation=None)
        if not self.exists():
            self.create()

        parser.read(self.config_path)
        decimalplaces = parser.getint("GENERAL", "decimalplaces")
        copytoclipboard = parser.getboolean("GENERAL", "copytoclipboard")
        userfriendly = parser.getboolean("GENERAL", "userfriendly")
        free_format = parser.getboolean("GENERAL", "free_format")

        return KalcConfig(decimalplaces, copytoclipboard, userfriendly, free_format)

    def create(self) -> None:
        """Creating a configuration file"""

        folder, file = os.path.split(self.config_path)

        parser = ConfigParser(allow_no_value=True)
        parser["GENERAL"] = {
            "; DECIMALPLACES - Round a result up to <decimalplaces> decimal places. Values: integer 1,2,3": None,
            "decimalplaces": "2",
            "; COPYTOCLIPBOARD - Need to copy results into clipboard. Values: True/False": None,
            "copytoclipboard": True,
            "; USERFRIENDLY - Need to separate thousands with a space. Values: True/False": None,
            "userfriendly": True,
            "; FREE FORMAT - Can use free format of float ((11.984,01; 11,984.01; 11984,01; 11984.01)). Values: True/False": None,
            "free_format": False,
        }

        if not os.path.exists(self.plugin_path):
            os.mkdir(self.plugin_path)

        with open(self.config_path, "w+", encoding="utf-8") as configfile:
            parser.write(configfile)

        # click.echo(f"Path to ini file: {click.format_filename(self.config_path)} \n")
        # click.echo(click.style("INI file is created"))
        # click.echo(
        #     click.style("!!! Fill in all the required parameters in the file !!! \n")
        # )
        # click.launch(self.config_path)
        # click.pause()

    def exists(self) -> bool:
        """Checking if config file exists"""
        return os.path.exists(self.config_path)

    @property
    def set_path(self) -> Union[str, pathlib.Path]:
        """Setting path for saving config file"""
        path = click.get_app_dir('kalc', roaming=False)
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

    def remove_config(self):
        """ Remove encryption keys """
        os.remove(self.config_path)

    def remove_plugin_folder(self):
        """ Remove encryption keys """
        shutil.rmtree(self.plugin_path)
