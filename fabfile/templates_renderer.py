from fabric.main import *
"""
Renders templates onto the server
"""


def create_prod_settings(config, data):
    """
    Recreates the prod_settings.py file
    in the project
    """
    filename='prod_settings.jinja'
    destination=os.path.join(config.git_path, config.name, config.name, 'prod_settings.py')
    context={ 'data': data }
    _put_template(filename, destination, context)


def create_prod_wsgi(config, data):
    filename='prod_wsgi.jinja'
    destination=os.path.join(config.git_path, config.name, config.name, 'prod_wsgi.py')
    context={ 'data': data }
    _put_template(filename, destination, context)


def _put_template(filename, destination, context):
    files.upload_template(
        filename=filename,
        destination=destination,
        context=context,
        use_jinja=True,
        template_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
    )