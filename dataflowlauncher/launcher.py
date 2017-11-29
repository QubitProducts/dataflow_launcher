import logging
import subprocess

import os.path

from os import getcwd
from clint.textui import colored

from dataflowlauncher.constants import POM
from dataflowlauncher.parsers.cli_parsers.cli_parser_main import get_cli_argument_parser, get_updated_config_dict, \
    run_cli_setup_actions, get_updated_launch_params
from dataflowlauncher.parsers.config_parsers.config_parser_main import parse_config_file, get_jar_parameter_dict
from dataflowlauncher.utils.git_utils import assert_clean_master
from dataflowlauncher.utils.pom_utils import parse_pom, get_jar_filename
from dataflowlauncher.utils.parameter_utils import format_launch_parameters

logging.basicConfig(level=logging.INFO)


def main():
    parser = get_cli_argument_parser()
    args, unknown_args = parser.parse_known_args()
    logging.debug("Parsed CLI arguments - args: %s, unknown args: %s", args, unknown_args)

    if not args.ignore_checks:
        assert_clean_master(getcwd())

    run(args, unknown_args, getcwd())


def run(args, unknown_args, exec_path):
    conf_file = os.path.join(exec_path, args.file)

    """Read configuration with config readers, update configuration with cli parsers"""
    config = parse_config_file(conf_file)
    config.update(get_updated_config_dict(config, args))

    """Run setup actions"""
    run_cli_setup_actions(config, args)

    """Generate parameters with config readers, update parameters with cli parsers """
    parameter_dict = get_jar_parameter_dict(config)
    parameter_dict.update(get_updated_launch_params(parameter_dict, args))

    parameter_list = get_formatted_launch_parameters(parameter_dict, args.unknown_arguments, unknown_args)
    print_launch_parameters(parameter_list)

    jar_file = args.jar_file
    if jar_file is None or not jar_file.strip():
        """Figure out jar file from pom"""
        pom_path = os.path.join(exec_path, config[POM])
        artifact, version = parse_pom(pom_path)
        assert artifact != ''
        assert version != ''
        jar_file = get_jar_filename(args.jar_path, artifact, version)

    return run_with_parameters(parameter_list, args.bypass_prompt,
                               exec_path, jar_file)


def get_formatted_launch_parameters(parameter_dict, add_unknown_args, unknown_args):
    """Format launch param dict and add on unknown args if needed"""
    parameter_list = format_launch_parameters(parameter_dict)

    if add_unknown_args:
        """Adding on the unknown arguments"""
        for argument in unknown_args:
            parameter_list.append(argument)

    return parameter_list


def print_launch_parameters(parameters):
    if parameters is None:
        return

    print("===== Setting Parameters ====")
    params_and_values = [(i[0], '='.join(i[1:])) for i in
                         [v.split('=') for v in parameters] if
                         len(i) > 1]
    for (var, val) in sorted(params_and_values, key=lambda x: x[0]):
        if var == '--projectId':
            val = colored.red(val, bold=True)
        print("\t{} = {}".format(var, val))
    print()


def run_with_parameters(parameter_list, bypass_prompt, exec_path, jar_filename):
    if not bypass_prompt:
        print()
        input("####### Press enter to continue with the deployment #######\n")

    cmd = ["/usr/bin/java"]
    jar_path = os.path.join(exec_path, jar_filename)
    logging.info("Launching job via external process")
    cmd.extend(["-jar", jar_path])
    subprocess.call(cmd + parameter_list)
    return ""


if __name__ == '__main__':
    main()
