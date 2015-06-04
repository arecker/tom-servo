from fabric.api import *


class HandShake(object):
    def __init__(self, config):
        run('echo "Hello from $(hostname)!"')
        sudo('echo "SUDO hello from $(hostname)"')

