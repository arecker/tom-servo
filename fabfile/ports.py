from fabric.contrib import files
from fabric.api import *
import yaml


def get_port(name):
    if not files.exists('~/ports.yml'):
        run('echo "localhost: 7999" > ~/ports.yml')
    data = yaml.load(run('cat ~/ports.yml'))

    try:
        return data[name]
    except KeyError:
        if len(data) is 0:
            highest_port = 7999
        else:
            highest_port = data[max(data, key=data.get)]
        data[name] = str(int(highest_port) + 1)
        files.append('~/ports.yml', '{0}: {1}'.format(name, data[name]))
        return data[name]