from fabric.api import *
from fabric.contrib.files import exists
import os


def main(config, input_model):
    if not config:
        raise "So... where's your config?"
    if not input_model:
        raise "Forgot to ask questions"

    # Ensure git path is there
    if not exists(config.git_path):
        run('mkdir -p {0}'.format(config.git_path))

    # Clone repo if it doesn't exist
    repo_path = os.path.join(config.git_path, input_model.name)
    if not exists(repo_path):
        with cd(config.git_path):
            run('git clone {0} {1}'.format(input_model.url, input_model.name))


def verify(config, input_model):
    exists(config.git_path) # git path exists
    exists(os.path.join(config.git_path, input_model.name)) # repo path exists