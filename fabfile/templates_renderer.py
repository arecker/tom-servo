from fabric.main import *
from fabric.api import *
from data import Data
from ports import get_port
"""
Renders templates onto the server
"""


def _put_template(filename, destination, context, use_sudo=False):
    files.upload_template(
        filename=filename,
        destination=destination,
        context=context,
        use_jinja=True,
        template_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates'),
        use_sudo=use_sudo
    )


class ProdDjangoSettings:
    def __init__(self, config, db_pass):
        import settings_reader
        data = Data()
        data.password = db_pass
        if not data.password:
            data.password = settings_reader.get_db_password(config)
        data.name = config.name
        data.domain = config.domain
        data.secret = settings_reader.get_secret_key(config)
        self.data = data
        self.config = config


    def upload(self):
        filename='prod_settings.jinja'
        destination=os.path.join(self.config.git_path, self.config.name, self.config.name, 'prod_settings.py')
        context={ 'data': self.data }
        _put_template(filename, destination, context)


class NginxConfig:
    def __init__(self, config):
        self.data = Data()
        self.name = config.name
        self.data.domain = config.domain
        self.data.static_path = os.path.join(config.git_path, config.name, 'prod_static', '')
        self.data.port = get_port(config.name)


    def upload(self):
        filename='nginx.jinja'
        destination=os.path.join('/etc/nginx/sites-available', self.name)
        context={ 'data': self.data }
        _put_template(filename, destination, context, use_sudo=True)
        return self


    def activate(self):
        """
        TODO: Create symlink in sites-enabled and reload server
        """
        enabled_path = os.path.join('/etc/nginx/sites-enabled/{0}'.format(self.name))
        if not files.exists(enabled_path):
            sudo('ln -s /etc/nginx/sites-available/{0} /etc/nginx/sites-enabled/{0}'.format(self.name))
        sudo('nginx -s reload')


class SystemdService:
    def __init__(self, config):
        self.data = Data()
        self.data.name = config.name
        self.data.user = config.user
        self.data.working_dir = os.path.join(config.git_path, config.name)
        self.data.gunicorn = os.path.join(config.env_path, config.name, 'bin/gunicorn')
        self.data.wsgi = config.name + '.wsgi'
        self.data.port = get_port(config.name)


    def upload(self):
        filename='systemd.jinja'
        destination=os.path.join('/etc/systemd/system/', self.data.name + '.service')
        context={ 'data': self.data }
        _put_template(filename, destination, context, use_sudo=True)
        return self


    def activate(self):
        sudo('systemctl daemon-reload')
        sudo('systemctl enable {0} && systemctl restart {0}'.format(self.data.name))