import logging
import subprocess

import os.path

from os import getcwd
from clint.textui import colored

from dataflowlauncher.constants import POM, JAR_NAME_FORMAT
from dataflowlauncher.parsers.cli_parsers.cli_parser_main import get_cli_argument_parser, get_updated_config_dict, \
    run_cli_setup_actions, get_updated_launch_params
from dataflowlauncher.parsers.config_parsers.config_parser_main import parse_config_file, get_jar_parameter_dict
from dataflowlauncher.utils.git_utils import has_dirty_branch
from dataflowlauncher.utils.pom_utils import parse_pom, get_jar_filename
from dataflowlauncher.utils.parameter_utils import format_launch_parameters

logging.basicConfig(level=logging.INFO)


def main():
    parser = get_cli_argument_parser()
    args = parser.parse_args()
    logging.debug("Parsed CLI arguments - args: %s", args)

    if not args.ignore_git and has_dirty_branch(getcwd()):
        print("GIT check failed: clean branch or --ignore_git flag required")
        exit(1)

    run(args, getcwd())


def run(args, exec_path):
    conf_file = os.path.join(exec_path, args.file)

    """Read configuration with config readers, update configuration with cli parsers"""
    config = parse_config_file(conf_file)
    config.update(get_updated_config_dict(config, args))

    """Run setup actions"""
    run_cli_setup_actions(config, args)

    """Generate parameters with config readers, update parameters with cli parsers """
    parameter_dict = get_jar_parameter_dict(config)

    updated_parameters = get_updated_launch_params(parameter_dict, args)

    updated_parameter_dict = dict(parameter_dict)
    updated_parameter_dict.update(updated_parameters)

    parameter_list = get_formatted_launch_parameters(updated_parameter_dict)

    print_launch_parameters(updated_parameter_dict)
    print_updated_parameters(updated_parameters, parameter_dict)

    jar_file = args.jar_file
    if jar_file is None or not jar_file.strip():
        """Figure out jar file from pom"""
        pom_path = os.path.join(exec_path, config[POM])
        artifact, version = parse_pom(pom_path)
        jar_file = get_jar_filename(args.jar_path, artifact, version, config[JAR_NAME_FORMAT])

    return run_with_parameters(parameter_list, args.bypass_prompt,
                               exec_path, jar_file)


def get_formatted_launch_parameters(parameter_dict):
    """Format launch param dict"""
    parameter_list = format_launch_parameters(parameter_dict)

    return parameter_list


def print_launch_parameters(parameters):
    if parameters is None:
        return

    print("===== Setting Parameters ====")
    for (var, val) in sorted(parameters.items(), key=lambda x: x[0]):
        if var == 'project':
            val = colored.red(val, bold=True)
        print("\t--{} = {}".format(var, val))
    print()


def print_updated_parameters(updated_parameters, old_parameters):
    if updated_parameters is None or len(updated_parameters) == 0:
        return

    print("===== Overridden Parameters ====")
    for (var, val) in sorted(updated_parameters.items(), key=lambda x: x[0]):
        if var == 'project':
            val = colored.red(val, bold=True)
        print("\t{}: old value = {} ----replaced-by---> new value = {}".format(var,old_parameters[var], val))
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
