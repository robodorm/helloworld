from datetime import datetime
from os import getenv

from setuptools import setup, find_packages


def requires():
    return open("requirements.txt").readlines()


dev = []

if getenv("ENVIRON") != "PROD":
    dev = ["pyresttest"]

setup(
    name='helloapp',
    version="1.0.0",
    description='▌│█║▌║▌║ Hello app ║▌║▌║█│▌',
    url='github.com/robodorm',
    packages=find_packages(exclude=("test*",)),
    include_package_data=True,
    install_requires=requires() + dev,
    zip_safe=False,
    test_suite='tests',
)