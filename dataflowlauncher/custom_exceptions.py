class ConfigFileNotFoundException(Exception):
    """Raise when config file is not found"""


class PomParseError(Exception):
    """Raise when the POM file cannot be parsed"""
