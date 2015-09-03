from fabric.api import env
import yaml


class Config:
    host_error = """Error: please specify

host:
  {name}: 'some-host'

in your config
"""

    def __init__(self, path):
        env['use_ssh_config'] = True
        with open(path) as file:
            self.data = yaml.load(file)

    def _set_host(self, name):
        self.data['host'] = name

    def password(self, password):
        env['password'] = password
        return self

    def prod(self):
        try:
            host = self.data['host']['prod']
            env['host_string'] = host
            self._set_host(host)
            return self
        except (KeyError, AttributeError, TypeError):
            print(self.host_error.format(name='prod'))
            exit(0)

    def stage(self):
        try:
            host = self.data['host']['stage']
            env['host_string'] = host
            self._set_host(host)
            return self
        except (KeyError, AttributeError, TypeError):
            print(self.host_error.format(name='stage'))
            exit(0)
