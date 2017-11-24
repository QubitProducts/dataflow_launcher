"""Required cli arguments"""
from dataflowlauncher.parsers.cli_parsers.base_cli_parser import CliParser


class RequiredCliParser(CliParser):
    def add_arguments_group(self, parser):
        required_parsers = parser.add_argument_group(
            "required",
            description="Pass in the required parameters for the dataflow")
        required_parsers.add_argument(
            '-f', '--file', default='flow.conf', type=str,
            help='Configuration file name. Default: flow.conf')

    def run_preprocessing(self, config_dict, cli_args):
        return None

    def get_updated_params_from_args(self, config_dict, cli_args):
        return None

    def get_updated_config_from_args(self, config_dict, cli_args):
        return None
