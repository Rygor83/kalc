#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------
import click
import ctypes
# import os
import errno
from appdirs import *
from collections import namedtuple
from configparser import ConfigParser

KalcConfig = namedtuple('KalcConfig', ['decimalround', 'copytoclipboard', 'userfriendly'])


class Config(object):

    def __init__(self):
        self.ini_name = 'kalc_config.ini'
        self.config_path = os.path.join(self.set_path(), self.ini_name)

    def read(self):
        """Return KalcConfig object after reading config file."""
        parser = ConfigParser()
        if not self.exists():
            self.create()
        else:
            a = parser.read(self.config_path)

            decimalround = parser.get('GENERAL', 'decimalround')
            copytoclipboard = parser.getboolean('GENERAL', 'copytoclipboard')
            userfriendly = parser.getboolean('GENERAL', 'userfriendly')

            return KalcConfig(decimalround, copytoclipboard, userfriendly)

    def create(self):
        parser = ConfigParser()
        parser['GENERAL'] = {'decimalround': 'number, 2 , 3',
                             'copytoclipboard': 'True or False',
                             'userfriendly': 'True or False'}

        with open(self.config_path, 'w+') as configfile:
            parser.write(configfile)

        click.echo('Путь: %s \n' % click.format_filename(self.config_path))
        click.echo(click.style('INI файл создан'))
        click.echo(click.style('!!! Заполните все требуемые параметры в файле !!! \n'))
        click.launch(self.config_path)

    def exists(self):
        if os.path.exists(self.config_path):
            return True
        else:
            return False

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
