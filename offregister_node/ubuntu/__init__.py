from functools import partial
from itertools import imap

from fabric.contrib.files import exists
from fabric.operations import run, _run_command
from fabric.context_managers import cd, shell_env

from offregister_fab_utils.apt import apt_depends
from offutils import it_consumes


def install_node0(*args, **kwargs):
    apt_depends('curl', 'build-essential')

    run_cmd = partial(_run_command, sudo=kwargs.get('node_sudo', kwargs.get('use_sudo', False)))
    if exists('n'):
        return
    run_cmd('mkdir -p Downloads')
    print "install_node0::kwargs.get('use_sudo', False) =", kwargs.get('use_sudo', False)
    print 'install_node0::kwargs =', kwargs
    with cd('Downloads'):
        script = 'n-install.bash'
        if not exists(script):
            run_cmd('curl -L https://git.io/n-install -o {}'.format(script))
        run_cmd('bash ./{script} -y \'{version}\''.format(script=script,
                                                          version=kwargs.get('node_version', 'latest')))


def install_global_npm_packages1(*args, **kwargs):
    if 'npm_global_packages' in kwargs:
        with shell_env(PATH='$HOME/n/bin:$PATH'):
            print "install_global_npm_packages1::kwargs.get('use_sudo', False) =", kwargs.get('use_sudo', False)
            _run_command('npm install -g {packages}'.format(packages=' '.join(kwargs['npm_global_packages']),
                                                            sudo=kwargs.get('node_sudo',
                                                                            kwargs.get('use_sudo', False))))
