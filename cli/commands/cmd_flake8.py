import subprocess

import click

@click.command()
@click.option('--skip-init/--no-skip-init', default=False,
               help='要Skip __init__.py 吗?')
@click.argument('path', default='myapp')
def cli(skip_init, path):
    """
      使用flake8检查代码是否符合规范
    """
    flake8_flag_exclude=''
    if skip_init:
        flake8_flag_exclude=' --exclude __init__.py'
    cmd = 'flake8 {}{}'.format(path, flake8_flag_exclude)
    return subprocess.call(cmd, shell=True)
