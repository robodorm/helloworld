import logging
from os import getenv

from setuptools import setup, find_packages

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_commit_sha():
    default_not_in_git_version = "0"

    def get_from_git():
        import subprocess
        try:
            sha = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
        except BaseException:
            logger.warning("Project not in git or git not installed in the system")
            sha = default_not_in_git_version
        return sha

    try:
        import git
    except ImportError:
        logger.info("Please consider to setup python git support: 'pip install gitpython'")
        sha = get_from_git()
    else:
        try:
            repo = git.Repo(search_parent_directories=False)
        except git.exc.InvalidGitRepositoryError:
            sha = default_not_in_git_version
        else:
            sha = repo.head.object.hexsha

    return sha


def requirements():
    requirements_dev = []

    if not getenv("ENVIRON", "").startswith("PROD"):
        try:
            requirements_dev = open("requirements-dev.txt").readlines()
        except BaseException:
            logger.warning("A file with development modules not found or not readable. "
                           "It means that tests could not work! "
                           "Please add this file with name 'requirements-dev.txt'")

    return open("helloapp/requirements.txt").readlines() + requirements_dev


MAJOR_VERSION = 1
APP_VERSION = getenv("APP_VERSION")

if not APP_VERSION:
    APP_VERSION = f"{MAJOR_VERSION}.{get_commit_sha()}"
    logger.warning("the APP_VERSION env variable not fond. "
                   "App will be tagged with new version AUTOMATICALLY! "
                   f"New version: {APP_VERSION}")

setup(
    name='mkg',
    version=APP_VERSION,
    description='▌│█║▌║▌║ HelloWorld ║▌║▌║█│▌',
    author='rbd',
    url='github.com/robodorm',
    packages=find_packages(exclude=("test*",)),
    include_package_data=True,
    install_requires=requirements(),
    zip_safe=False,
    test_suite='tests',
)
