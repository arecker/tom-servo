from fabric.contrib import files


def append_if_needed(domain):
    if files.contains('/etc/hosts', domain):
        pass
    else:
        files.append('/etc/hosts', '\n127.0.0.1       {0}'.format(domain), use_sudo=True)