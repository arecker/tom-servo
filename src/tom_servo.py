import click
import yaml
from fabric.api import env


class Config(object):
    def __init__(self, path=None):
        if path:
            return self._build_from_file(path)
        return None


    def _build_from_file(self, path):
        with open(path) as file:
            data = yaml.load(file)
            return self._build_config(data)


    def _build_from_input(self):
        pass


    def _build_config(self, data):
        for item in data:
            if item == 'env':
                env_place = data['env']
                for i in data[item]:
                    setattr(env, i, env_place[i])
            else:
                setattr(self, item, data[item])


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
    from servos import HandShake
    HandShake(Config(config))


@cli_main.command()
@click.option('config', '--config', type=click.Path(), help='path to config file')
def bootstrap(config):
    """
    bootstrap a server
    """
    c = Config(config)
    from servos import PathCreator
    PathCreator(c)
    
    from servos import DependencyInstaller
    DependencyInstaller(c)

    from servos import FirewallBuilder
    FirewallBuilder(c)


@cli_main.command()
@click.option('config', '--config', type=click.Path(), help='path to config file')
def django(config):
    """
    deploy a django application
    """
    c = Config(config)
    from servos import DjangoApplication
    DjangoApplication(c)


@cli_main.command()
def test():
    """
    test something random
    """
    import jinja2
    import os
    path = os.path.join(os.path.dirname(__file__),"templates")
    print('PATH: ' + path)
    loader=jinja2.FileSystemLoader(path)
    env = jinja2.Environment(loader=loader)
    template = env.get_template('test.txt')
    print template.render()


if __name__ == '__main__':
    cli_main()
