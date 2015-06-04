from fabric.api import *


class HandShake(object):
    def __init__(self, config):
        run('echo "Hello from $(hostname)!"')
        sudo('echo "SUDO hello from $(hostname)"')


class DependencyInstaller(object):
    def __init__(self, config):
        self._install_apt_deps(config.dependencies)
        self._install_npm_deps(config.npm_dependencies)


    def _install_apt_deps(self, packages):
        for package in packages:
            sudo('apt-get install -y {0}'.format(package))


    def _install_npm_deps(self, packages):
        for package in packages:
            sudo('npm install -g {0}'.format(package))


class DjangoApplication(object):
    def __init__(self, config):
        pass

