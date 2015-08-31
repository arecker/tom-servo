import click
from __init__ import Config


@click.group()
def main():
    """
    the snarky linux server assistant
    """
    pass


@main.command()
@click.argument('config', type=click.Path(exists=True))
def prod(config):
    """
    execute a servo on the production host
    """
    from servos.sanity import HandshakeServo
    HandshakeServo(Config(config)).run()


@main.command()
@click.argument('config', type=click.Path(exists=True))
def stage(config):
    """
    execute a servo on the staging host
    """
    pass


if __name__ == '__main__':
    main(prog_name='tom-servo')
