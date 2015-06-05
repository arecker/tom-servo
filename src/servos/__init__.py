from fabric.api import *
from fabric.contrib import files


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


class FirewallBuilder(object):
    def __init__(self, config):
        sudo('ufw default deny incoming')
        sudo('ufw default allow outgoing')
        for p in config.ports:
            sudo('ufw allow {0}'.format(p))
        sudo('ufw --force enable')
        sudo('service ufw restart') # TODO: should probably restart this with the new systemd syntax


class HostWriter(object):
    def __init__(self, config):
        if files.contains('/etc/hosts', config.domain):
            pass
        else:
            files.append('/etc/hosts', '127.0.0.1    {0}'.format(config.domain, use_sudo=True)


class DjangoApplication(object):
    def __init__(self, config):
        pass

