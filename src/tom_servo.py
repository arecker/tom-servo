import click
import yaml
from fabric.api import env
from src import config


def build_config_from_file(path=None):
    with open(path) as file:
        data = yaml.load(file)
        for item in data:
            if item == 'env': # set fabric environment
                env_place = data['env']
                for i in data[item]:
                    setattr(env, i, env_place[i])
            else:
                setattr(config, item, data[item])




@click.command()
@click.option('config_file', '--config', type=click.Path(), help='path to config file')
def cli_main(config_file):
    """
    tom-servo: the snarky linux server assistant
    """
    if not config:
        print('Please supply a valid --config path')
        exit()

    try:
        build_config_from_file(config_file)
        { 'handshake': handshake,
          'bootstrap': bootstrap,
          'static': static,
          'django': django }[config.profile]()
    except Exception as e:
        print(e)
        exit(1)



def handshake():
    """
    say hello to the server
    """
    from helpers import HandShake
    HandShake()


def bootstrap():
    """
    bootstrap a server
    """
    from helpers import PathCreator
    PathCreator()
    
    from helpers import DependencyInstaller
    DependencyInstaller()

    from helpers import FirewallBuilder
    FirewallBuilder()


def django():
    """
    deploy a django application
    """
    from helpers import DjangoApplication
    DjangoApplication()


def static():
    """
    deploy a static site
    """
    from helpers import StaticWebsite
    StaticWebsite()


if __name__ == '__main__':
    cli_main()
