from fabric.api import *


def main(config):
    for package in config.dependencies:
        sudo('apt-get install -y {0}'.format(package))
    _verify(config)


def _verify(config):
    for package in config.dependencies:
        sudo('dpkg-query -l {0}'.format(package))