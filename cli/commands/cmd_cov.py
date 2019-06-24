import subprocess

import click

@click.command()
@click.argument('path', default='myapp')
def cli(path):
    """
    检查coverage
    """
    cmd = 'py.test --cov-report term-missing --cov {0}'.format(path)
    return subprocess.call(cmd, shell=True)
