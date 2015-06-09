from fabric.api import *
from fabric.contrib import files
import yaml
import random
import string


class HandShake(object):
    def __init__(self, config):
        run('echo "Hello from $(hostname)!"')
        sudo('echo "SUDO hello from $(hostname)"')


class DependencyInstaller(object):
    """
    passes packages listed in config
    into aptitude and npm for global installation
    """
    def __init__(self, config):
        self._install_apt_deps(config.dependencies)
        self._install_npm_deps(config.npm_dependencies)


    def _install_apt_deps(self, packages):
        for package in packages:
            sudo('apt-get install -y {0}'.format(package))


    def _install_npm_deps(self, packages):
        for package in packages:
            sudo('npm install -g {0}'.format(package))


class PathCreator(object):
    """
    creates all config items that match "*_path"
    """
    def __init__(self, config):
        for path in filter(lambda x: '_path' in x and not x.startswith('__'), dir(config)):
            run('mkdir -p {0}'.format(getattr(config, path)))
            assert files.exists(getattr(config, path))


class FirewallBuilder(object):
    """
    sets up firewall with ufw
    opens up ports specified in config
    """
    def __init__(self, config):
        sudo('ufw default deny incoming')
        sudo('ufw default allow outgoing')
        for p in config.ports:
            sudo('ufw allow {0}'.format(p))
        sudo('ufw --force enable')
        sudo('service ufw restart') # TODO: should probably restart this with the new systemd syntax


class HostWriter(object):
    """
    writes a domain to /etc/hosts if it doesn't exist yet
    """
    def __init__(self, config):
        if files.contains('/etc/hosts', config.domain):
            pass
        else:
            files.append('/etc/hosts', '127.0.0.1    {0}'.format(config.domain, use_sudo=True))


class PortManager(object):
    """
    tracks occupied ports in a config file on the server
    """
    def __init__(self, config):
        self._touch_file()
        self._read_file()
        return self._get_highest_port(config.name)


    def _touch_file(self):
        if not files.exists('~/ports.yml'):
            run('echo "localhost: 7999" > ~/ports.yml')


    def _read_file(self, name):
        self.data = yaml.load(run('cat ~/ports.yml'))


    def _get_highest_port(self, name):
        try:
            return self.data[name]
        except KeyError:
            if len(self.data) is 0:
                highest_port = 7999
            else:
                highest_port = self.data[max(self.data, key=self.data.get)]
            self.data[name] = str(int(highest_port) + 1)
            files.append('~/ports.yml', '{0}: {1}'.format(name, self.data[name]))
            return self.data[name]


class PasswordGenerator:
    @classmethod
    def _generate_hash(cls, length):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


    @staticmethod
    def generate_django_password():
        return PasswordGenerator._generate_hash(100)


    @staticmethod
    def generate_db_password():
        return PasswordGenerator._generate_hash(10)


class DjangoApplication:
    pass