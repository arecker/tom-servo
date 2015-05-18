from fabric.api import *


def bootstrap(config):
    """
    Verifies database - creates it if needed
    Returns authentication password
    """
    if _database_exists(config.name):
        print('exists')
        import settings_reader
        return settings_reader.get_db_password(config)
    else:
        return _create_db(config.name)


def _database_exists(db_name):
    return sudo('psql -lqt | cut -d \| -f 1 | grep -w {0} | wc -l'.format(db_name),  user='postgres') == '1'


def _create_db(name):
    import passwords
    db_pass = passwords.get_password()
    sudo('psql -c "CREATE DATABASE {0};"'.format(name), user='postgres')
    sudo('psql -c "CREATE USER {0} WITH PASSWORD {1};"'.format(name, '\'' + db_pass + '\''), user='postgres')
    sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE {0} TO {0};"'.format(name), user='postgres')
    if not _database_exists(name):
        raise 'Database was not created, yo'
    return db_pass