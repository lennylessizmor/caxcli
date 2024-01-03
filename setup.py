from setuptools import setup

setup(
    name='caxcli',
    version='0.1.0',
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
