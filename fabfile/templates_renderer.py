"""
Renders templates onto the server
"""


def create_prod_settings(ui, data):
    """
    Recreates the prod_settings.py file
    in the project
    """
    print(_render('prod_settings.jinja'))


def _render(name, data={}):
    from jinja2 import Environment, FileSystemLoader
    _environment = Environment(loader=FileSystemLoader('templates'))
    t = _environment.get_template(name)
    return t.render(data)