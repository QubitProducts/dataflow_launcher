from dataflowlauncher.constants import (
    POM,
    JAR_NAME_FORMAT
)
from dataflowlauncher.parsers.config_parsers.base_config_parser import ConfigParser


class PomConfigParser(ConfigParser):
    def parse_config_file(self):
        configuration = dict()
        configuration[POM] = self.conf.get_string('pom.name', 'pom.xml')
        configuration[JAR_NAME_FORMAT] = self.conf.get_string('pom.generated_jar_name', '{artifact}-{version}.jar')
        return configuration

    def get_jar_params_from_conf(self, config):
        return dict()
