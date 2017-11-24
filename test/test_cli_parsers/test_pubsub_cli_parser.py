from unittest import TestCase, main
from unittest.mock import patch

from argparse import ArgumentParser
from dataflowlauncher.parsers.cli_parsers.pubsub_cli_parser import (
    JOB_PROJECT_ID,
    JOB_NAME,
    PUBSUB_READ,
    PUBSUB_WRITE,
    PubsubCliParser
)


class TestPubSubCliParser(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_add_arguments_group(self):
        parser = ArgumentParser(prog="PROG")
        input_arg_str = "-u -i -c"
        PubsubCliParser().add_arguments_group(parser)
        args = parser.parse_args(input_arg_str.split())
        self.assertTrue(args.create_missing_output_topics)
        self.assertTrue(args.create_missing_subscriptions)
        self.assertTrue(args.create_missing_input_topics)

    @patch("dataflowlauncher.parsers.cli_parsers." \
           "pubsub_cli_parser.setup_pubsub", autospec=True)
    def test_run_preprocessing(self, mock_setup_pubsub):
        mock_setup_pubsub.return_value = None
        sample_config = {
            PUBSUB_READ: {
                "foo": "bar"
            },
            PUBSUB_WRITE: {
                "fooWrite": "barWrite"
            },
            JOB_PROJECT_ID: "test_project_id",
            JOB_NAME: "test_name"
        }

        parser = ArgumentParser(prog="PROG")
        input_arg_str = "-u -i -c"
        cli_parser = PubsubCliParser()
        cli_parser.add_arguments_group(parser)
        cli_args = parser.parse_args(input_arg_str.split())
        cli_parser.run_preprocessing(sample_config, cli_args)

    def test_get_pubsub_topics(self):
        sample_config = {
            PUBSUB_WRITE: {
                "foo": "bar"
            }
        }
        reference_result = [("foo", "bar")]
        returned_result = PubsubCliParser.get_pubsub_topics(sample_config)
        self.assertListEqual(reference_result, returned_result)

    def test_get_pubsub_subscriptions(self):
        sample_config = {
            PUBSUB_READ: {
                "foo": "bar"
            },
            JOB_PROJECT_ID: "test_project_id",
            JOB_NAME: "test_name"
        }
        reference_result = [
            ("foo",
             "bar_test_name",
             "bar")
        ]
        returned_result = PubsubCliParser.get_pubsub_subscriptions(
            sample_config)
        self.assertListEqual(reference_result, returned_result)


if __name__ == '__main__':
    main()
