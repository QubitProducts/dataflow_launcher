import logging

from dataflowlauncher.parsers.cli_parsers.base_cli_parser import CliParser

class OverrideArgumentsParser(CliParser):
    def add_arguments_group(self, parser):
        override_arguments_parser = parser.add_argument_group(
            "overrides",
            description="Pass in the parameters to override those derived from config file and previous cli-parsers")
        override_arguments_parser.add_argument(
            '--override_arguments', nargs='*',
            help='List of parameters to override from those derived from the config file, as a space-separated list of the form <fieldName>=<value>')

    def run_preprocessing(self, config_dict, cli_args):
        return None

    def get_updated_params_from_args(self, parameter_dict, cli_args):
        new_params = dict()
        for additional_arg in cli_args.override_arguments:
            split = additional_arg.split('=')
            if len(split) == 2:
                new_params[split[0]] = split[1]
            else:
                logging.error("Ignoring override argument {}, as not in the form <key>=<value>".format(additional_arg))

        return new_params

    def get_updated_config_from_args(self, config_dict, cli_args):
        return None