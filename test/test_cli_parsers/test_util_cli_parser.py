from unittest import TestCase, main
from argparse import ArgumentParser
from dataflowlauncher.parsers.cli_parsers.util_cli_parser\
    import UtilCliParser


class TestUtilCliParser(TestCase):
    def test_add_arguments_group(self):
        parser = ArgumentParser(prog="PROG")
        input_arg_str = "--ignore_git --bypass_prompt"
        UtilCliParser().add_arguments_group(parser)
        args = parser.parse_args(input_arg_str.split())
        self.assertTrue(args.ignore_git)
        self.assertTrue(args.bypass_prompt)

    def test_java_runtime_default(self):
        parser = ArgumentParser(prog="PROG")
        UtilCliParser().add_arguments_group(parser)
        args = parser.parse_args()
        self.assertEqual(args.java_runtime, "/usr/bin/java")

    def test_java_runtime(self):
        parser = ArgumentParser(prog="PROG")
        java_runtime = "/alternative/java"
        input_arg_str = "--java_runtime=" + java_runtime
        UtilCliParser().add_arguments_group(parser)
        args = parser.parse_args(input_arg_str.split())
        self.assertEqual(args.java_runtime, java_runtime)

if __name__ == '__main__':
    main()
