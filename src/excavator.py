from fabric.api import *
from fabric.contrib.files import exists
import os
import pipes
from src.servos import PasswordGenerator
from src import config


"""
A really silly module that reads settings out of
Django settings.py files on the server
"""
def get_db_password():
    """
    Digs database password out of prod_settings.py
    If we have gotten here, the file *should* exist
    """
    with cd(os.path.join(config.git_path, config.name, config.name)):
        py_command = 'import prod_settings as p; print(p.DATABASES["default"]["PASSWORD"])'
        return run(_build_command(py_command))


def get_secret_key():
    """
    Returns the prod_settings secret key if it exists
    If not, generates one
    """
    if exists(os.path.join(config.git_path, config.name, config.name, 'prod_settings.py')):
        with cd(os.path.join(config.git_path, config.name, config.name)):
            py_command = 'import prod_settings as p; print(p.SECRET_KEY)'
            return run(_build_command(py_command))
    return PasswordGenerator.generate_django_password()



def get_installed_apps():
    """
    Returns the INSTALLED_APPS list
    from settings.py
    """
    with cd(os.path.join(config.git_path, config.name, config.name)):
        py_command = 'import settings as s; print("__".join(s.INSTALLED_APPS))'
        return run(_build_command(py_command)).split('__')


def _build_command(py_command):
    return 'python -c {0}'.format(pipes.quote(py_command))
