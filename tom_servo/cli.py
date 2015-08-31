import click


@click.group(invoke_without_command=True)
@click.argument('config', type=click.Path(exists=True), required=False)
def main(config=None):
    """
    the snarky linux server assistant
    """
    if not config:
        print('config help')
        exit()
    print('Config: {0}'.format(config))


if __name__ == '__main__':
    main(prog_name='tom-servo')
