import random
import string

from fabric.api import *
from fabric.contrib import files
from fabric.operations import *
import yaml
import os

from src import config


class HandShake(object):
    def __init__(self):
        run('echo "Hello from $(hostname)!"')
        sudo('echo "SUDO hello from $(hostname)"')


class DependencyInstaller(object):
    """
    passes packages listed in config
    into aptitude and npm for global installation
    """
    def __init__(self):
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
    def __init__(self):
        for path in filter(lambda x: '_path' in x and not x.startswith('__'), dir(config)):
            run('mkdir -p {0}'.format(getattr(config, path)))
            assert files.exists(getattr(config, path))


class EnvironmentCreator(object):
    """
    instantiates a python virtualenv for the project
    """
    def __init__(self):
        with cd(config.env_path):
            if not files.exists('./{0}'.format(config.name)):
                run('virtualenv --no-site-packages {0}'.format(config.name))


class GitUpdater(object):
    def __init__(self):
        repo_path = os.path.join(config.git_path, config.name)
        if not files.exists(repo_path):
            with cd(config.git_path):
                run('git clone {0} {1}'.format(config.url, config.name))

        # Clean and pull if it does
        else:
            with cd(repo_path):
                run('git reset --hard origin/master')
                run('git pull origin master')


class FirewallBuilder(object):
    """
    sets up firewall with ufw
    opens up ports specified in config
    """
    def __init__(self):
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
    def __init__(self):
        if files.contains('/etc/hosts', config.domain):
            pass
        else:
            #files.append('/etc/hosts', '127.0.0.1    {0}'.format(config.domain, use_sudo=True)) Not working?
            sudo('echo "127.0.0.1     {0}" >> /etc/hosts'.format(config.domain))


class PortManager(object):
    """
    tracks occupied ports in a config file on the server
    """
    def __init__(self):
        self._touch_file()
        self._read_file()


    def _touch_file(self):
        if not files.exists('~/ports.yml'):
            run('echo "localhost: 7999" > ~/ports.yml')


    def _read_file(self):
        self.data = yaml.load(run('cat ~/ports.yml'))


    def get_highest_port(self):
        name = config.name
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


class DjangoMaker(object):
    def __init__(self):
        with cd(os.path.join(config.git_path, config.name)):
            if files.exists('makefile'):
                with prefix('source {0}'.format(os.path.join(config.env_path, config.name, 'bin/activate'))):
                    run('make')


class DatabaseCreator(object):
    """
    Ensures the app database is created
    - generates a password if it is not
    - finds the password if it is
    Either way, adds the password to the config
    """
    def __init__(self):
        name = config.name
        if self._database_exists(name):
            from src.excavator import get_db_password
            password = get_db_password()
        else:
            password = self._create_db(name)
        setattr(config, 'db_pass', password)


    def _database_exists(self, db_name):
        return sudo('psql -lqt | cut -d \| -f 1 | grep -w {0} | wc -l'.format(db_name),  user='postgres') == '1'


    def _create_db(self, name):
        db_pass = PasswordGenerator.generate_db_password()
        sudo('psql -c "CREATE DATABASE {0};"'.format(name), user='postgres')
        sudo('psql -c "CREATE USER {0} WITH PASSWORD {1};"'.format(name, '\'' + db_pass + '\''), user='postgres')
        sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE {0} TO {0};"'.format(name), user='postgres')
        if not self._database_exists(name):
            raise 'Database was not created, yo'
        return db_pass


class SiteUpdater(object):
    """
    takes a path to a tar.gz from the config
    updates the site on the webroot with the payload
    """
    def __init__(self):
        self._put_payload()
        self._open_payload()
        self._clean_up()


    def _put_payload(self):
        put(config.payload, '/tmp/{0}.tar.gz'.format(config.name))


    def _open_payload(self):
        www_path = os.path.join(config.www_path, config.name)
        sudo('mkdir -p {0}'.format(www_path))
        sudo('tar xvf /tmp/{0}.tar.gz -C {1}'.format(config.name, www_path))


    def _clean_up(self):
        sudo('rm /tmp/{0}.tar.gz'.format(config.name))
        sudo('chown -R www-data {0}'.format(config.www_path))


class StaticWebsite:
    def __init__(self):
        from src.renderer import NginxStaticConfig
        SiteUpdater()
        NginxStaticConfig().upload().activate()
        HostWriter()


class DjangoApplication:
    def __init__(self):
        from src.renderer import ProdDjangoSettings, SystemdService, NginxDjangoConfig
        GitUpdater()
        EnvironmentCreator()
        DatabaseCreator()
        ProdDjangoSettings().upload()
        DjangoMaker()
        SystemdService().upload().activate()
        NginxDjangoConfig().upload().activate()
        HostWriter()
