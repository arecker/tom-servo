from servos import BaseServo, run


class HandshakeServo(BaseServo):
    def run(self):
        run('echo "Hello, {0}"'.format(self.config.prod_host))
