from dataflowlauncher.constants import (
    FLOW
)
from dataflowlauncher.parsers.config_parsers.base_config_parser import ConfigParser


class FlowConfigParser(ConfigParser):
    def parse_config_file(self):
        configuration = dict()
        configuration[FLOW] = self.get_dict_from_config_tree(self.conf, "flow")
        return configuration

    def get_jar_params_from_conf(self, config):
        return config[FLOW]
