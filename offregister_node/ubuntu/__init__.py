from functools import partial
from itertools import imap

from fabric.contrib.files import exists
from fabric.operations import run, _run_command
from fabric.context_managers import cd, shell_env

from offregister_fab_utils.apt import apt_depends
from offutils import it_consumes


def install_node0(*args, **kwargs):
    apt_depends('curl', 'build-essential')

    run_cmd = partial(_run_command, sudo=kwargs.get('use_sudo', False))
    run_cmd('mkdir -p Downloads')
    if exists('n'):
        return
    with cd('Downloads'):
        script = 'n-install.bash'
        if not exists(script):
            run('curl -L https://git.io/n-install -o {}'.format(script))
        run_cmd('bash ./{script} -y \'{version}\''.format(script=script,
                                                          version=kwargs.get('node_version', 'latest')))


def install_npm_package(*args, **kwargs):
    if 'npm_global_packages' in kwargs:
        if shell_env(PATH='$HOME/n/bin:$PATH'):
            it_consumes(imap(lambda package: _run_command('npm install -g {package}'.format(package=package),
                                                          sudo=kwargs.get('use_sudo', False))),
                        kwargs['npm_global_packages'])
