from offregister_fab_utils.apt import apt_depends

from offregister_node.utils import install_global_npm_packages, install_node


def install_node0(c, node_version="latest", *args, **kwargs):
    apt_depends(c, "curl", "build-essential")

    return install_node(node_version=node_version, **kwargs)


def install_global_npm_packages1(c, *args, **kwargs):
    return install_global_npm_packages(**kwargs)
