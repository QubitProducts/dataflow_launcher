"""Pubsub related CLI args"""
import logging

from dataflowlauncher.constants import (
    JOB_PROJECT_ID,
    JOB_NAME,
    PUBSUB_READ,
    PUBSUB_READ_VERBATIM,
    PUBSUB_WRITE
)
from dataflowlauncher.parsers.cli_parsers.base_cli_parser import CliParser
from dataflowlauncher.utils.pub_sub_utils import (
    setup_pubsub,
    get_formatted_subscription
)


class PubsubCliParser(CliParser):
    def add_arguments_group(self, parser):
        pubsub_parsers = parser.add_argument_group(
            "pubsub",
            description="Pass in the PubSub parameters for the dataflow")
        pubsub_parsers.add_argument(
            '-c', '--create_missing_output_topics', action='store_true',
            help='Create missing output PubSub topics. Default: false')
        pubsub_parsers.add_argument(
            '-i', '--create_missing_input_topics', action='store_true',
            help='Create missing input PubSub topics. Default: false')
        pubsub_parsers.add_argument(
            '-u', '--create_missing_subscriptions', action='store_true',
            help='Create missing input PubSub subscriptions. Default: false')

    def run_preprocessing(self, config_dict, cli_args):
        pubsub_topics = self.get_pubsub_topics(config_dict)
        pubsub_subscriptions = self.get_pubsub_subscriptions(config_dict)
        setup_pubsub(
            config_dict[JOB_PROJECT_ID], pubsub_topics, pubsub_subscriptions,
            cli_args.create_missing_output_topics,
            cli_args.create_missing_subscriptions,
            cli_args.create_missing_input_topics)

    def get_updated_params_from_args(self, config_dict, cli_args):
        return None

    def get_updated_config_from_args(self, config_dict, cli_args):
        return None

    @staticmethod
    def get_pubsub_topics(config):
        formatted_topics = []
        for topic_arg_name, topic_suffix in config[PUBSUB_WRITE].items():
            formatted_topics.append((topic_arg_name, topic_suffix))
        return formatted_topics

    @staticmethod
    def get_pubsub_subscriptions(config):
        formatted_subs = []
        for sub_arg_name, topic_prefix in config[PUBSUB_READ].items():
            sub = get_formatted_subscription(topic_prefix, config[JOB_NAME])
            logging.info(
                "setting formatted sub: %s:%s:%s", sub_arg_name, sub,
                topic_prefix)
            formatted_subs.append((sub_arg_name, sub, topic_prefix))
        return formatted_subs

