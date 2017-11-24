from abc import (
    ABCMeta,
    abstractmethod
)


class CliParser(metaclass=ABCMeta):
    @abstractmethod
    def add_arguments_group(self, parser):
        """Use to define and register arguments to the cli parser"""
        pass

    @abstractmethod
    def run_preprocessing(self, config_dict, cli_args):
        """Use to run any setup methods that need to happen before the flow gets launched"""
        pass

    @abstractmethod
    def get_updated_params_from_args(self, config_dict, cli_args):
        """Use to add or overwrite any parameters than will be passed to the launch command"""
        pass

    @abstractmethod
    def get_updated_config_from_args(self, config_dict, cli_args):
        """Used to add or overwrite configuration"""
        pass
