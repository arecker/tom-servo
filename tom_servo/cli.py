import click
from __init__ import Config


@click.group()
def main():
    """
    the snarky linux server assistant
    """
    pass


@main.command()
@click.option('--password', prompt='sudo password', hide_input=True,
              confirmation_prompt=True)
@click.argument('config', type=click.Path(exists=True))
def prod(config, password):
    """
    execute a servo on the production host
    """
    from servos.sanity import HandshakeServo
    c = Config(config).password(password).prod()
    HandshakeServo(c).run()


@main.command()
@click.option('--password', prompt='sudo password', hide_input=True,
              confirmation_prompt=True)
@click.argument('config', type=click.Path(exists=True))
def stage(config, password):
    """
    execute a servo on the staging host
    """
    from servos.sanity import HandshakeServo
    c = Config(config).password(password).stage()
    HandshakeServo(c).run()


if __name__ == '__main__':
    main(prog_name='tom-servo')
