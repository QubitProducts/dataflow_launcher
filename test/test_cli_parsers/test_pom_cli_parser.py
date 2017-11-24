from unittest import TestCase, main
from argparse import ArgumentParser
from dataflowlauncher.parsers.cli_parsers.pom_cli_parser import PomCliParser


class TestPomCliParser(TestCase):
    def test_add_arguments_group(self):
        parser = ArgumentParser(prog="PROG")
        input_arg_str = "-j foo.jar --jar_file bar.jar"
        PomCliParser().add_arguments_group(parser)
        args = parser.parse_args(input_arg_str.split())
        self.assertEqual("foo.jar", args.jar_path)
        self.assertEqual("bar.jar", args.jar_file)


if __name__ == '__main__':
    main()
