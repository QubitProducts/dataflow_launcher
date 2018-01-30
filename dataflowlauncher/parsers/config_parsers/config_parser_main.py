"""This is where we register configuration parsers"""
import logging

from dataflowlauncher.parsers.config_parsers.flow_config_parser import FlowConfigParser
from dataflowlauncher.parsers.config_parsers.pom_config_parser import PomConfigParser
from dataflowlauncher.parsers.config_parsers.pubsub_config_parser import PubSubConfigParser
from dataflowlauncher.parsers.config_parsers.required_config_parser import RequiredConfigParser

CONFIG_PARSER_ITERABLE = (
    FlowConfigParser,
    RequiredConfigParser,
    PomConfigParser,
    PubSubConfigParser
)


def parse_config_file(config_filename, config_parsers=None):
    if config_parsers is None:
        config_parsers = CONFIG_PARSER_ITERABLE
    config = dict()
    for parser_class in config_parsers:
        parser = parser_class()
        logging.info("Parsing configuration with %s parser",
                     parser.__class__.__name__)
        config.update(parser.get_config_parameters(config_filename))
    return config


def get_jar_parameter_dict(config, config_parsers=None):
    if config_parsers is None:
        config_parsers = CONFIG_PARSER_ITERABLE
    parameter_dict = dict()
    for parser_class in config_parsers:
        parser = parser_class()
        logging.info("Preparing jar args with %s parser",
                     parser.__class__.__name__)
        parameter_dict.update(parser.get_jar_params_from_conf(config))
    return parameter_dict
