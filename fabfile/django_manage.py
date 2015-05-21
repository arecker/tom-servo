from fabric.api import *
from fabric.main import files
import os


def make(config):
    with cd(os.path.join(config.git_path, config.name)):
        if files.exists('makefile'):
            with prefix('source {0}'.format(os.path.join(config.env_path, config.name, 'bin/activate'))):
                run('make')
        else:
            _migrate(config)
            _collect_static(config)


def _migrate(config):
    command = 'makemigrations'
    _execute_manage_command(config, command)
    command = 'migrate'
    _execute_manage_command(config, command)


def _collect_static(config):
    command = 'collectstatic --noinput'
    _execute_manage_command(config, command)


def _execute_manage_command(config, command):
    py_path = os.path.join(config.env_path, config.name, 'bin/python')
    with cd(os.path.join(config.git_path, config.name)):
        run('{0} manage.py {1}'.format(py_path, command))