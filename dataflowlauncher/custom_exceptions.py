class ConfigFileNotFoundException(Exception):
    """Raise when config file is not found"""


class JobLaunchError(Exception):
    """Raise when job cannot be executed"""


class JobIdParseError(Exception):
    """Raise when job id cannot be parsed"""
