import logging
from rootpath import get_absolute_path
from unittest import TestCase, main
from pyhocon import ConfigFactory

from dataflowlauncher.parsers.config_parsers.pom_config_parser import (
    POM,
    JAR_NAME_FORMAT,
    PomConfigParser
)


class TestPomConfigParser(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.parser = PomConfigParser()
        self.test_file_name = get_absolute_path("_testing/test_conf.conf")

    def test_parse_config_file(self):
        parsed_config = self.parser.get_config_parameters(self.test_file_name)
        reference_config = {POM: "test_pom.xml", JAR_NAME_FORMAT: "{artifact}-{version}-dist.jar"}
        self.assertDictEqual(parsed_config, reference_config)

    def test_populates_default_values_when_not_in_config(self):
        self.parser.conf = ConfigFactory.from_dict(dict())

        expected_defaults = {POM: "pom.xml", JAR_NAME_FORMAT: "{artifact}-{version}.jar"}
        defaults = self.parser.parse_config_file()

        self.assertDictEqual(expected_defaults, defaults)

    def test_get_jar_params_from_conf(self):
        parsed_config = self.parser.get_config_parameters(self.test_file_name)
        jar_args = self.parser.get_jar_params_from_conf(parsed_config)
        reference_args = dict()
        self.assertDictEqual(reference_args, jar_args)


if __name__ == '__main__':
    main()
