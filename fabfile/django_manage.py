from fabric.api import *
import os


def migrate(config):
    command = 'makemigrations'
    _execute_manage_command(config, command)
    command = 'migrate'
    _execute_manage_command(config, command)


def collect_static(config):
    command = 'collectstatic --noinput'
    _execute_manage_command(config, command)


def _execute_manage_command(config, command):
    py_path = os.path.join(config.env_path, config.name, 'bin/python')
    with cd(os.path.join(config.git_path, config.name)):
        run('{0} manage.py {1}'.format(py_path, command))