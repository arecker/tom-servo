from fabric.api import *


# Get Rood Directory
import os
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


# Get Raw Config Data
import json
CONFIG = None
with open(os.path.join(PROJECT_ROOT, '..', 'config.json')) as file:
    CONFIG = json.load(file)


# Setup fab environment
for item in CONFIG['env']:
    setattr(env, item, CONFIG['env'][item])


class InputModel(object):
    """
    Everything we'll need from the user
    Gets handed back and forth between tasks
    """
    def __init__(self):
        pass


@task
def handshake(model=None):
    """
    Say hello to the server
    """
    run('hostname')
    print('Handshake successful')


if __name__ == '__main__':
    import sys
    from fabric.main import main
    sys.argv = ['fab', '-f', __file__, 'handshake']
    main()
