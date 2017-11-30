"""This is where we register argument parsers"""
from argparse import RawTextHelpFormatter, ArgumentParser

from dataflowlauncher.parsers.cli_parsers.override_arguments_cli_parser import OverrideArgumentsParser
from dataflowlauncher.parsers.cli_parsers.pom_cli_parser import PomCliParser
from dataflowlauncher.parsers.cli_parsers.pubsub_cli_parser import PubsubCliParser
from dataflowlauncher.parsers.cli_parsers.required_cli_parser import RequiredCliParser
from dataflowlauncher.parsers.cli_parsers.util_cli_parser import UtilCliParser

CLI_PARSER_ITERABLE = (
    RequiredCliParser,
    PomCliParser,
    PubsubCliParser,
    UtilCliParser,
    OverrideArgumentsParser # This needs to be invoked last to ensure expected behaviour of parameter overrides
)


def get_cli_argument_parser(cli_parser_iterable=None):
    if cli_parser_iterable is None:
        cli_parser_iterable = CLI_PARSER_ITERABLE

    parser = ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description='''Dataflow launch helper script.''')

    for cli_class in cli_parser_iterable:
        cli_parser = cli_class()
        cli_parser.add_arguments_group(parser)

    return parser


def run_cli_setup_actions(config, cli_args, cli_parser_iterable=None):
    if cli_parser_iterable is None:
        cli_parser_iterable = CLI_PARSER_ITERABLE

    for cli_class in cli_parser_iterable:
        cli_parser = cli_class()
        cli_parser.run_preprocessing(config, cli_args)


def get_updated_config_dict(config, cli_args, cli_parser_iterable=None):
    updated_config = dict()
    if cli_parser_iterable is None:
        cli_parser_iterable = CLI_PARSER_ITERABLE

    for cli_class in cli_parser_iterable:
        cli_parser = cli_class()
        to_update = cli_parser.get_updated_config_from_args(config, cli_args)
        if to_update is not None:
            updated_config.update(to_update)

    return updated_config


def get_updated_launch_params(parameter_dict, cli_args, cli_parser_iterable=None):
    if cli_parser_iterable is None:
        cli_parser_iterable = CLI_PARSER_ITERABLE

    updated_param_dict = dict()
    for cli_class in cli_parser_iterable:
        cli_parser = cli_class()
        to_update = cli_parser.get_updated_params_from_args(parameter_dict, cli_args)
        if to_update is not None:
            updated_param_dict.update(to_update)

    return updated_param_dict
