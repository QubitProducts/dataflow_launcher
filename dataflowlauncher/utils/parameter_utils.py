"""Utils to create the command to pass to the jar"""


def format_parameter(key, value):
    return "--{}={}".format(key, value)


def format_launch_parameters(variable_dict):
    return [format_parameter(key, val) for key, val in variable_dict.items()]