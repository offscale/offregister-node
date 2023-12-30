from fabric.contrib.files import exists
from offregister_fab_utils.fs import cmd_avail


def install_node(c, node_version="latest", *args, **kwargs):
    run_cmd = (
        c.sudo if kwargs.get("node_sudo", kwargs.get("use_sudo", False)) else c.run
    )
    n_prefix = kwargs.get("N_PREFIX", run_cmd("echo $HOME/n", hide=True))
    if cmd_avail(c, "n") and not exists(
        c,
        runner=c.run,
        path="{n_prefix}/n/versions/node/{version}".format(
            n_prefix=n_prefix, version=node_version
        ),
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


def install_global_npm_packages(c, *args, **kwargs):
    n_prefix = kwargs.get("N_PREFIX", "$HOME/n")

    if "npm_global_packages" in kwargs:
        env = dict(PATH="{n_prefix}/bin:$PATH".format(n_prefix=n_prefix))
        packages = " ".join(kwargs["npm_global_packages"])
        (c.sudo if kwargs.get("node_sudo", kwargs.get("use_sudo", False)) else c.run)(
            "npm install -g {packages}".format(
                packages=packages,
            )
        )
        return {"Node.js globally installed": packages}
