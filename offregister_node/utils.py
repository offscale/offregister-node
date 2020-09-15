from functools import partial

from fabric.context_managers import shell_env
from fabric.contrib.files import exists
from fabric.operations import _run_command
from offregister_fab_utils.fs import cmd_avail


def install_node(node_version="latest", *args, **kwargs):
    run_cmd = partial(
        _run_command, sudo=kwargs.get("node_sudo", kwargs.get("use_sudo", False))
    )
    n_prefix = kwargs.get("N_PREFIX", run_cmd("echo $HOME/n", quiet=True))
    if cmd_avail("n") and not exists(
        "{n_prefix}/n/versions/node/{version}".format(
            n_prefix=n_prefix, version=node_version
        )
    ):
        run_cmd("n {version}".format(version=node_version))
    else:
        run_cmd(
            "curl -L https://git.io/n-install"
            " | N_PREFIX='{n_prefix}' bash -s -- -y '{version}'".format(
                n_prefix=n_prefix, version=node_version
            )
        )

    return {"Node.js version installed": node_version}


def install_global_npm_packages(*args, **kwargs):
    n_prefix = kwargs.get("N_PREFIX", "$HOME/n")

    if "npm_global_packages" in kwargs:
        with shell_env(PATH="{n_prefix}/bin:$PATH".format(n_prefix=n_prefix)):
            packages = " ".join(kwargs["npm_global_packages"])
            _run_command(
                "npm install -g {packages}".format(
                    packages=packages,
                    sudo=kwargs.get("node_sudo", kwargs.get("use_sudo", False)),
                )
            )
            return {"Node.js globally installed": packages}
