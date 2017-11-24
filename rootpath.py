from os.path import dirname, join

ROOT_DIR = dirname(__file__)

def get_absolute_path(value):
    return join(ROOT_DIR, value)