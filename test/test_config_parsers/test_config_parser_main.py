from unittest import TestCase, main
from rootpath import get_absolute_path

from dataflowlauncher.parsers.config_parsers.config_parser_main import (
    get_jar_parameter_dict,
    parse_config_file
)
from dataflowlauncher.parsers.config_parsers.base_config_parser import\
    ConfigParser


class TestConfigParser(ConfigParser):
    def parse_config_file(self):
        return dict(test_config_var="foo")

    def get_jar_params_from_conf(self, config_dict):
        return dict(test_jar_arg="bar")


class TestConfigParserMain(TestCase):
    def setUp(self):
        self.config_file_name = get_absolute_path("_testing/test_conf.conf")

    def test_parse_config_file(self):
        config_parsers = (TestConfigParser, )
        parsed_config = parse_config_file(self.config_file_name,
                                          config_parsers)
        reference_result = dict(test_config_var="foo")
        self.assertDictEqual(reference_result, parsed_config)

    def test_get_jar_parameter_dict(self):
        config_parsers = (TestConfigParser, )
        jar_args = get_jar_parameter_dict(dict(), config_parsers)
        reference_result = dict(test_jar_arg="bar")
        self.assertDictEqual(reference_result, jar_args)


if __name__ == '__main__':
    main()
