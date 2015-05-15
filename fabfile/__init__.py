from fabric.api import *


# Get Rood Directory
import os
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


# Build Config and Env
class Config:
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
    """
    import dependencies
    dependencies.main(Config)
    print('Bootstrap successful')


@task
def git_update(ui=None):
    """
    Refreshes a git repository
    """
    if not ui:
        ui = UserInput
    import git
    git.main(Config, ui)


@task
def python_env(ui=None):
    """
    Creates/Updates a projects virtualenv
    """
    if not ui:
        ui = UserInput()
    git_update(ui)
    import virtualenv
    virtualenv.main(Config, ui)


if __name__ == '__main__':
    import sys
    from fabric.main import main
    sys.argv = ['fab', '-f', __file__, 'python_env'] # whatever task you are testing
    main()
