from unittest import TestCase, main
from argparse import ArgumentParser

from dataflowlauncher.parsers.cli_parsers.override_arguments_cli_parser import OverrideArgumentsParser


class TestOverrideArgumentsParser(TestCase):
    def test_add_arguments_group(self):
        parser = ArgumentParser(prog="PROG")
        input_arg_str = "--override_arguments key1=value1 key2=value2"
        OverrideArgumentsParser().add_arguments_group(parser)
        args = parser.parse_args(input_arg_str.split())
        self.assertEqual(["key1=value1", "key2=value2"], args.override_arguments)

    def test_updates_params(self):
        parser = ArgumentParser(prog="PROG")
        input_arg_str = "--override_arguments key1=value1 key2=value2"
        OverrideArgumentsParser().add_arguments_group(parser)
        args = parser.parse_args(input_arg_str.split())

        params = {'key1':'oldvalue1', 'key2': 'oldvalue2'}
        new_params = OverrideArgumentsParser().get_updated_params_from_args(params, args)
        params.update(new_params)

        expected_params = {'key1':'value1', 'key2': 'value2'}

        self.assertEqual(params, expected_params)

if __name__ == '__main__':
    main()