#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------
import click
import errno
from appdirs import *
from collections import namedtuple
from configparser import ConfigParser

KalcConfig = namedtuple('KalcConfig', ['decimalround', 'copytoclipboard', 'userfriendly'])


class Config(object):

    def __init__(self):
        self.ini_name = 'kalc_config.ini'
        self.config_path = os.path.join(self.set_path, self.ini_name)

    def read(self):
        """Return KalcConfig object after reading config file."""
        parser = ConfigParser(interpolation=None)
        if not self.exists():
            self.create()

        parser.read(self.config_path)
        decimalround = parser.getint('GENERAL', 'decimalround')
        copytoclipboard = parser.getboolean('GENERAL', 'copytoclipboard')
        userfriendly = parser.getboolean('GENERAL', 'userfriendly')

        return KalcConfig(decimalround, copytoclipboard, userfriendly)

    def create(self):
        parser = ConfigParser()
        parser['GENERAL'] = {'decimalround': "Round a result up to <decimalround> decimal. Values: integer 1,2,3",
                             'copytoclipboard': "Need to copy results into clipboard. Values: True/False",
                             'userfriendly': "Need to separate thousands with a space. Values: True/False"}

        with open(self.config_path, 'w+') as configfile:
            parser.write(configfile)

        click.echo('Path to ini file: %s \n' % click.format_filename(self.config_path))
        click.echo(click.style('INI file is created'))
        click.echo(click.style('!!! Fill in all the required parameters in the file !!! \n'))
        click.launch(self.config_path)
        click.pause()

    def exists(self):
        if os.path.exists(self.config_path):
            return True
        else:
            return False

    @property
    def set_path(self):
        path = user_data_dir('kalc', appauthor=False)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        return path

    def open_config(self):
        click.launch(self.config_path)
