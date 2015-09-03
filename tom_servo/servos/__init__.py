from fabric.api import (
    run
)


assert hasattr(run, '__call__')


class BaseServo(object):
    def __init__(self, config):
        self.config = config.data

    def run(self):
        raise NotImplementedError('Servo requires a \'run\' routine')

    def nuke(self):
        raise NotImplementedError('Servo requires a \'nuke\' routine')
