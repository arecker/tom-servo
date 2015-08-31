from fabric.api import env
import yaml


class Config:
    def __init__(self, path):
        with open(path) as file:
            data = yaml.load(file)
            for item in data:
                setattr(self, item, data[item])
        env['use_ssh_config'] = True
        env['host_string'] = self.prod_host
