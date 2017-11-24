import logging
from rootpath import get_absolute_path
from unittest import TestCase, main

from dataflowlauncher.parsers.config_parsers.flow_config_parser import (
    FLOW
)
from dataflowlauncher.parsers.config_parsers.flow_config_parser import \
    FlowConfigParser


class TestFlowConfigParser(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.parser = FlowConfigParser()
        self.test_file_name = get_absolute_path("_testing/test_conf.conf")

    def test_parse_config_file(self):
        reference_config = {
            FLOW: {
                "metricsReporterPort": 9125,
                "metricsReporterType": "test_reporterType",
                "metricsEnabled": "true"
            }
        }
        parsed_config = self.parser.get_config_parameters(self.test_file_name)
        self.assertDictEqual(parsed_config, reference_config)

    def test_get_jar_params_from_conf(self):
        sample_config = {FLOW : "test"}
        jar_args = self.parser.get_jar_params_from_conf(sample_config)
        self.assertEqual("test", jar_args)


if __name__ == '__main__':
    main()
