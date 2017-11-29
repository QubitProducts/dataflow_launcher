import logging

from dataflowlauncher.constants import (
    JOB_PROJECT_ID,
    JOB_NAME,
    PUBSUB_READ,
    PUBSUB_READ_VERBATIM,
    PUBSUB_WRITE
)
from dataflowlauncher.parsers.config_parsers.base_config_parser import ConfigParser
from dataflowlauncher.utils.pub_sub_utils import (
    get_topic_name,
    get_formatted_subscription,
    get_subscription_name
)


class PubSubConfigParser(ConfigParser):
    def parse_config_file(self):
        configuration = dict()
        configuration[PUBSUB_READ] = self.get_dict_from_config_tree(
            self.conf, 'pubsub.read')
        configuration[PUBSUB_WRITE] = self.get_dict_from_config_tree(
            self.conf, 'pubsub.write')
        configuration[PUBSUB_READ_VERBATIM] = self.get_dict_from_config_tree(
            self.conf, 'pubsub.read_verbatim')

        return configuration

    def get_jar_params_from_conf(self, config):
        variables = dict()
        variables.update(self.add_topic_variables(config))
        variables.update(self.add_subscription_variables(config))
        variables.update(self.add_subscription_verbatim(config))
        return variables

    @staticmethod
    def add_topic_variables(config):
        result = dict()
        for topic_arg_name, topic_suffix in config[PUBSUB_WRITE].items():
            result[topic_arg_name] = get_topic_name(config[JOB_PROJECT_ID],
                                                    topic_suffix)

        return result

    @staticmethod
    def add_subscription_variables(config):
        result = dict()
        for sub_arg_name, topic in config[PUBSUB_READ].items():
            result[sub_arg_name] = get_subscription_name(
                config[JOB_PROJECT_ID],
                get_formatted_subscription(topic, config[JOB_NAME]))
            logging.info("setting formatted sub: %s:%s:%s", sub_arg_name,
                         result[sub_arg_name], topic)

        return result

    @staticmethod
    def add_subscription_verbatim(config):
        result = dict()
        read_verbatim = config[PUBSUB_READ_VERBATIM]
        if 'project_id' in read_verbatim:
            subscription_project = read_verbatim['project_id']
            read_verbatim = dict(read_verbatim)
            del read_verbatim['project_id']
        else:
            subscription_project = config[JOB_PROJECT_ID]

        for sub_arg_name, sub in read_verbatim.items():
            result[sub_arg_name] = get_subscription_name(
                subscription_project, sub)

        return result
