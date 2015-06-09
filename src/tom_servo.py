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




@click.group()
def cli_main():
    """
    tom-servo: the snarky linux server assistant
    """
    pass


@cli_main.command()
@click.option('config', '--config', type=click.Path(), help='path to config file')
def handshake(config):
    """
    say hello to the server
    """
    build_config_from_file(config)
    from helpers import HandShake
    HandShake()


@cli_main.command()
@click.option('config', '--config', type=click.Path(), help='path to config file')
def bootstrap(config):
    """
    bootstrap a server
    """
    build_config_from_file(config)
    from helpers import PathCreator
    PathCreator()
    
    from helpers import DependencyInstaller
    DependencyInstaller()

    from helpers import FirewallBuilder
    FirewallBuilder()


@cli_main.command()
@click.option('config', '--config', type=click.Path(), help='path to config file')
def django(config):
    """
    deploy a django application
    """
    build_config_from_file(config)
    from helpers import DjangoApplication
    DjangoApplication()


@cli_main.command()
@click.option('config', '--config', type=click.Path(), help='path to config file')
def static(config):
    """
    deploy a static site
    """
    build_config_from_file(config)
    from helpers import StaticWebsite
    StaticWebsite()


if __name__ == '__main__':
    cli_main()
