from offregister_fab_utils.apt import apt_depends

from offregister_node.utils import install_node, install_global_npm_packages


def install_node0(node_version="latest", *args, **kwargs):
    apt_depends("curl", "build-essential")

    return install_node(node_version=node_version, **kwargs)


def install_global_npm_packages1(*args, **kwargs):
    return install_global_npm_packages(**kwargs)
