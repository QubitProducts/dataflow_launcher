"""Utility functions to manipulate git."""
import logging
from git import Repo

logging.basicConfig(level=logging.INFO)


def has_dirty_branch(repo_path):
    """ Ensures that repo is not dirty when deploying to production."""
    logging.debug('Asserting Production Checks')
    repo = Repo(repo_path)
    return repo.is_dirty()
