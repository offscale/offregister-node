from functools import partial

from fabric.contrib.files import exists
from fabric.operations import _run_command
from fabric.context_managers import cd, shell_env

from offregister_fab_utils.apt import apt_depends
from offregister_fab_utils.fs import cmd_avail


def install_node0(node_version='latest', *args, **kwargs):
    apt_depends('curl', 'build-essential')

    run_cmd = partial(_run_command, sudo=kwargs.get('node_sudo', kwargs.get('use_sudo', False)))
    if cmd_avail('n') and not exists('$HOME/n/n/versions/node/{version}'.format(version=node_version)):
        run_cmd('n {version}'.format(version=node_version))
    else:
        run_cmd('mkdir -p $HOME/Downloads')
        with cd('$HOME/Downloads'):
            script = 'n-install.bash'
            run_cmd('curl -L https://git.io/n-install -o {}'.format(script))
            run_cmd('bash ./{script} -y \'{version}\''.format(script=script,
                                                              version=node_version))

    return {'Node.js version installed': node_version}


def install_global_npm_packages1(*args, **kwargs):
    if 'npm_global_packages' in kwargs:
        with shell_env(PATH='$HOME/n/bin:$PATH'):
            packages = ' '.join(kwargs['npm_global_packages'])
            _run_command('npm install -g {packages}'.format(packages=packages,
                                                            sudo=kwargs.get('node_sudo',
                                                                            kwargs.get('use_sudo', False))))
            return {'Node.js globally installed': packages}
