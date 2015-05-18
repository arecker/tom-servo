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

    if not hasattr(Config, 'url'):
        Config.url = prompt('Git URL:')
    if not hasattr(Config, 'name'):
        Config.name = prompt('Repo Name:')
    if not hasattr(Config, 'domain'):
        Config.domain = prompt('Domain:')


def build_settings_data(db_pass):
    import settings_reader
    import passwords
    data = Data()
    data.password = db_pass
    if not data.password:
        data.password = settings_reader.get_db_password(Config)
    data.name = Config.name
    data.domain = Config.domain
    data.apps = settings_reader.get_installed_apps(Config)
    data.secret = settings_reader.get_secret_key(Config)
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
def deploy():
    """
    Deploys a django applications from a git URL
    """
    # Git
    import git
    git.main(Config)

    # Virtualenv
    import virtualenv
    virtualenv.main(Config)

    # Database
    import database
    db_pass = database.bootstrap(Config)

    # django settings
    data = build_settings_data(db_pass)
    import templates_renderer
    templates_renderer.create_prod_settings(Config, data)
    templates_renderer.create_prod_wsgi(Config, data)

    # django manage.py actions
    import django_manage
    django_manage.migrate(Config)
    django_manage.collect_static(Config)


if __name__ == '__main__':
    import sys
    from fabric.main import main
    sys.argv = ['fab', '-f', __file__, 'deploy'] # whatever task you are testing
    main()
