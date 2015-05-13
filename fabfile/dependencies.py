from fabric.api import *


def main(config):
    if not config:
        raise "So... where's your config?"
    for package in config.dependencies:
        sudo('apt-get install -y {0}'.format(package))


def verify(config):
    for package in config.dependencies:
        sudo('dpkg-query -l {0}'.format(package))