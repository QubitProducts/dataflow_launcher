from unittest import TestCase, main
from argparse import ArgumentParser
from dataflowlauncher.parsers.cli_parsers.util_cli_parser\
    import UtilCliParser


class TestUtilCliParser(TestCase):
    def test_add_arguments_group(self):
        parser = ArgumentParser(prog="PROG")
        input_arg_str = "--ignore_checks --bypass_prompt"
        UtilCliParser().add_arguments_group(parser)
        args = parser.parse_args(input_arg_str.split())
        self.assertTrue(args.ignore_checks)
        self.assertTrue(args.bypass_prompt)


if __name__ == '__main__':
    main()
