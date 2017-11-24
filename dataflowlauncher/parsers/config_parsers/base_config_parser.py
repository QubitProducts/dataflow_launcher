import os

from abc import (
    ABCMeta,
    abstractmethod
)
from pyhocon import ConfigFactory

from dataflowlauncher.custom_exceptions import ConfigFileNotFoundException


class ConfigParser(metaclass=ABCMeta):
    def __init__(self):
        self.conf = None
        self.config_to_jar_arguments = None

    def read_config_file(self, filename):
        self.conf = ConfigFactory.parse_file(filename)

    def get_config_parameters(self, filename):
        ConfigParser.check_file_exists(filename)
        self.read_config_file(filename)
        return self.parse_config_file()

    @staticmethod
    def get_dict_from_config_tree(config_tree, key):
        return {key: value for key, value in
                config_tree.get(key, {}).items()}

    @staticmethod
    def check_file_exists(filename):
        if not os.path.isfile(filename):
            message = "Config FileName: {} was not found".format(filename)
            raise ConfigFileNotFoundException(message)

    @abstractmethod
    def parse_config_file(self):
        pass

    @abstractmethod
    def get_jar_params_from_conf(self, config):
        pass

