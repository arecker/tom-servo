from setuptools import setup

setup(
    name="tom-servo",
    description="The snarky linux server assistant",
    version='1.0.0',
    url='http://github.com/arecker/tom-servo.git',
    author='Alex Recker',
    author_email='alex@reckerfamily.com',
    license='GPLv3',
    packages=[
        'src',
    ],
    entry_points={
        'console_scripts': ['tom-servo=src.tom_servo:cli_main']
    },
    include_package_data=True,
    install_requires=[
        'click',
        'fabric',
        'pyyaml',
        'jinja2'
    ]
)
