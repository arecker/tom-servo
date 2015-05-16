from fabric.api import *


def main(config):
    sudo('ufw default deny incoming')
    sudo('ufw default allow outgoing')
    for p in config.ports:
        sudo('ufw allow {0}'.format(p))
    sudo('ufw --force enable')
    sudo('service ufw restart')
    _verify(config)


def _verify(config):
    pass # I don't really know how to test this