from fabric.api import *
import os
import pipes


"""
A really silly module that reads settings out of
Django settings.py files on the server
"""
def get_db_password(config, ui):
    """
    Digs database password out of prod_settings.py
    If we have gotten here, the file *should* exist
    """
    with cd(os.path.join(config.git_path, ui.name, ui.name)):
        py_command = 'import prod_settings as p; print(p.DATABASES["default"]["PASSWORD"])'
        return run(_build_command(py_command))


def get_installed_apps(config, ui):
    """
    Returns the INSTALLED_APPS list
    from settings.py
    """
    with cd(os.path.join(config.git_path, ui.name, ui.name)):
        py_command = 'import settings as s; print("__".join(s.INSTALLED_APPS))'
        return run(_build_command(py_command)).split('__')


def _build_command(py_command):
    return 'python -c {0}'.format(pipes.quote(py_command))