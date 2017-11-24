"""Utility functions to manipulate git."""
import logging
from git import Repo

logging.basicConfig(level=logging.INFO)


def assert_clean_master(repo_path):
    """ Ensures that repo is not dirty when deploying to production."""
    logging.debug('Asserting Production Checks')
    repo = Repo(repo_path)
    assert not repo.is_dirty()
