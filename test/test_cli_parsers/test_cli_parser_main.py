from unittest import TestCase, main
from argparse import ArgumentParser
from dataflowlauncher.parsers.cli_parsers.cli_parser_main import (
    get_cli_argument_parser,
    run_cli_setup_actions,
    get_updated_config_dict,
    get_updated_launch_params
)
from dataflowlauncher.parsers.cli_parsers.base_cli_parser import CliParser


class TestCliParser(CliParser):
    def add_arguments_group(self, parser):
        pubsub_parsers = parser.add_argument_group("foo")
        pubsub_parsers.add_argument('-X', type=str)

    def run_preprocessing(self, config_dict, cli_args):
        global PRE_PROC_FLAG
        PRE_PROC_FLAG = True

    def get_updated_params_from_args(self, config_dict, cli_args):
        cli_value = getattr(cli_args, "X")
        if cli_value is not None:
            return dict(X=cli_value)

    def get_updated_config_from_args(self, config_dict, cli_args):
        config_value = getattr(cli_args, "X")
        if config_value is not None:
            return dict(X=config_value)


class TestCliParserMain(TestCase):
    def tearDown(self):
        if 'PRE_PROC_FLAG' in globals():
            del globals()['PRE_PROC_FLAG']

    def test_get_cli_argument_parser(self):
        parser = get_cli_argument_parser((TestCliParser, ))
        args = parser.parse_args("-X bar".split())
        self.assertEqual("bar", args.X)

    def test_run_cli_setup_actions(self):
        self.assertNotIn('PRE_PROC_FLAG', globals())
        run_cli_setup_actions(None, None, (TestCliParser, ))
        self.assertIn('PRE_PROC_FLAG', globals())
        self.assertTrue(PRE_PROC_FLAG)

    def test_get_updated_config_dict(self):
        configuration = dict(X="foo")
        parser = ArgumentParser(prog="PROG")
        TestCliParser().add_arguments_group(parser)
        cli_args = parser.parse_args("-X bar".split())
        result = get_updated_config_dict(configuration, cli_args,
                                         (TestCliParser,))
        self.assertNotEquals(configuration.get("X"), result.get("X"))
        self.assertDictEqual(dict(X="bar"), result)

    def test_get_updated_launch_params(self):
        configuration = dict(X="foo")
        parser = ArgumentParser(prog="PROG")
        TestCliParser().add_arguments_group(parser)
        cli_args = parser.parse_args("-X bar".split())
        result = get_updated_launch_params(configuration, cli_args,
                                           (TestCliParser, ))
        self.assertNotEquals(configuration.get("X"), result.get("X"))
        self.assertDictEqual(dict(X="bar"), result)


if __name__ == '__main__':
    main()
