from setuptools import setup
from version import __version__

setup(
    name='caxcli',
    version=__version__,
    py_modules=['caxcli'],
    install_requires=[
        'docopt>=0.6.2',
        'pandas',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        caxcli=caxcli:main
    ''',
)
