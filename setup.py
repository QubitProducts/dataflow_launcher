"""Setup the pypi package."""
from setuptools import setup, find_packages

REQUIREMENTS = [
    "GitPython==3.1.30",
    "gitdb2==3.0.1",
    "gcloud==0.18.3",
    "google-api-python-client==1.6.4",
    "pyhocon==0.3.38",
    "giturlparse.py==0.0.5",
    "requests>=2.20.0",
    "pylint==1.7.4",
    "oauth2client==4.1.2",
    "clint==0.5.1",
    "pex==1.2.13",
    "wheel==0.29.0"
]

TEST_REQUIREMENTS = [
    "clint==0.5.1",
    "nose==1.3.7",
    "pytest"
]

setup(name='dataflow_launcher',
      version='0.1.3',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      description='Launcher for Dataflow jobs',
      url='https://github.com/QubitProducts/dataflow_launcher',
      author='Qubit',
      author_email=['victor@qubit.com', 'bud@qubit.com'],
      install_requires=REQUIREMENTS,
      tests_require=TEST_REQUIREMENTS
      )
