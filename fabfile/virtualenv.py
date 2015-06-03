from fabric.api import *
from fabric.contrib.files import exists


def main(config):
    if not exists(config.env_path):
        run('mkdir -p {0}'.format(config.env_path))
    with cd(config.env_path):
        if not exists('./{0}'.format(config.name)):
            run('virtualenv --no-site-packages {0}'.format(config.name))
    _verify(config)


def _verify(config):
    if not exists(config.env_path):
        raise 'Environment directory was not written to disk'
    with cd(config.env_path):
        if not exists(config.name):
            raise 'Environment was not written to disk'
