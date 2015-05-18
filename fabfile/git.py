from fabric.api import *
from fabric.contrib.files import exists
import os


def main(config):
    # Ensure git path is there
    if not exists(config.git_path):
        run('mkdir -p {0}'.format(config.git_path))

    # Clone repo if it doesn't exist
    repo_path = os.path.join(config.git_path, config.name)
    if not exists(repo_path):
        with cd(config.git_path):
            run('git clone {0} {1}'.format(config.url, config.name))

    # Clean and pull if it does
    else:
        with cd(repo_path):
            run('git reset --hard origin/master')
            run('git pull origin master')

    _verify(config)


def _verify(config):
    exists(config.git_path) # git path exists
    exists(os.path.join(config.git_path, config.name)) # repo path exists