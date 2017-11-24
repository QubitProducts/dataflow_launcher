from unittest import TestCase, main
from argparse import ArgumentParser
from dataflowlauncher.parsers.cli_parsers.required_cli_parser\
    import RequiredCliParser


class TestRequiredCliParser(TestCase):
    def test_add_arguments_group(self):
        parser = ArgumentParser(prog="PROG")
        input_arg_str = "-f test.file"
        RequiredCliParser().add_arguments_group(parser)
        args = parser.parse_args(input_arg_str.split())
        self.assertEqual("test.file", args.file)

    def test_add_arguments_group_raise_exception(self):
        parser = ArgumentParser(prog="PROG")
        input_arg_str = "-f test.file"
        with self.assertRaises(SystemExit):
            parser.parse_args(input_arg_str.split())


if __name__ == '__main__':
    main()
