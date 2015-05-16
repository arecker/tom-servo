from fabric.api import *


# Get Rood Directory
import os
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


# Build Config and Env
class Config:
    pass


class Data:
    pass


import json
with open(os.path.join(PROJECT_ROOT, '..', 'config.json')) as file:
    data = json.load(file)
    for item in data:
        if item == 'env':
            env_place = data['env']
            for i in data[item]:
                setattr(env, i, env_place[i])
        else:
            setattr(Config, item, data[item])


class UserInput(object):
    """
    Everything we'll need from the user
    Gets handed back and forth between tasks
    """
    def __init__(self):
        self.url = prompt('Git URL:')
        self.name = prompt('Repo Name:')
        self.domain = prompt('Domain:')


def build_settings_data(db_pass, ui):
    import settings_reader
    import passwords
    data = Data()
    data.password = db_pass
    if not data.password:
        data.password = settings_reader.get_db_password(Config, ui)
    data.name = ui.name
    data.domain = ui.domain
    data.apps = settings_reader.get_installed_apps(Config, ui)
    data.secret = passwords.get_secret_key()
    return data


@task
def handshake():
    """
    Say hello to the server
    """
    run('hostname')
    print('Handshake successful')


@task
def bootstrap():
    """
    Install all needed linux packages on the server
    Sets up firewall
    """
    import dependencies
    dependencies.main(Config)
    import firewall
    firewall.main(Config)
    print('Bootstrap successful')


@task
def deploy(ui=None):
    """
    Deploys a django applications from a git URL
    """
    if not ui:
        ui = UserInput()

    # Git
    import git
    git.main(Config, ui)

    # Virtualenv
    import virtualenv
    virtualenv.main(Config, ui)

    # Database
    import database
    db_pass = database.bootstrap(Config, ui)

    # django settings
    data = build_settings_data(db_pass, ui)
    import templates_renderer
    templates_renderer.create_prod_settings(ui, data)


@task
def test():
    import templates_renderer
    templates_renderer.create_prod_settings('hi', 'hi')


if __name__ == '__main__':
    import sys
    from fabric.main import main
    sys.argv = ['fab', '-f', __file__, 'test'] # whatever task you are testing
    main()
