"""Pom related cli arguments'''"""
from dataflowlauncher.parsers.cli_parsers.base_cli_parser import CliParser


class PomCliParser(CliParser):
    def add_arguments_group(self, parser):
        pom_parsers = parser.add_argument_group(
            "pom", description="Pass in the POM parameters for the dataflow")
        pom_parsers.add_argument(
            '-j', '--jar_path', default='target', type=str,
            help='Relative path to JAR directory. Default: target')
        pom_parsers.add_argument(
            '--jar_file', type=str, help="Path to the JAR file. Overrides -j",
            default=None)

    def run_preprocessing(self, config_dict, cli_args):
        return None

    def get_updated_params_from_args(self, config_dict, cli_args):
        return None

    def get_updated_config_from_args(self, config_dict, cli_args):
        return None
