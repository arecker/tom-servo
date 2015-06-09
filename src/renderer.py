import os
from fabric.contrib import files
from fabric.api import *

from src.servos import PortManager
from src import config


class Data:
    pass


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
    def __init__(self):
        from src.servos import excavator
        log_path = os.path.join(config.log_path, config.name + '.log')
        run('touch {0}'.format(log_path))

        data = Data()
        data.password = config.db_pass
        if not data.password:
            data.password = excavator.get_db_password(config)
        data.name = config.name
        data.domain = config.domain
        data.email_password = config.email_password
        data.secret = excavator.get_secret_key()
        data.log = os.path.join(config.log_path, config.name + '.log')
        self.data = data


    def upload(self):
        filename='django.txt'
        destination=os.path.join(config.git_path, config.name, config.name, 'prod_settings.py')
        context={ 'data': self.data }
        _put_template(filename, destination, context)


class NginxConfig:
    def __init__(self):
        self.data = Data()
        self.name = config.name
        self.data.domain = config.domain
        self.data.static_path = os.path.join(config.git_path, config.name, 'prod_static', '')
        self.data.port = PortManager().get_highest_port()


    def upload(self):
        filename='django_nginx.txt'
        destination=os.path.join('/etc/nginx/sites-available', self.name)
        context={ 'data': self.data }
        _put_template(filename, destination, context, use_sudo=True)
        return self


    def activate(self):
        enabled_path = os.path.join('/etc/nginx/sites-enabled/{0}'.format(self.name))
        if not files.exists(enabled_path):
            sudo('ln -s /etc/nginx/sites-available/{0} /etc/nginx/sites-enabled/{0}'.format(self.name))
        sudo('nginx -s reload')


class SystemdService:
    def __init__(self):
        self.data = Data()
        self.data.name = config.name
        self.data.user = config.user
        self.data.working_dir = os.path.join(config.git_path, config.name)
        self.data.gunicorn = os.path.join(config.env_path, config.name, 'bin/gunicorn')
        self.data.wsgi = config.name + '.wsgi'
        self.data.port = PortManager().get_highest_port()


    def upload(self):
        filename='systemd.txt'
        destination=os.path.join('/etc/systemd/system/', self.data.name + '.service')
        context={ 'data': self.data }
        _put_template(filename, destination, context, use_sudo=True)
        return self


    def activate(self):
        sudo('systemctl daemon-reload')
        sudo('systemctl enable {0} && systemctl restart {0}'.format(self.data.name))