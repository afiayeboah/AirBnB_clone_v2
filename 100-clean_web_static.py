#!/usr/bin/python3
"""
Fabric script for cleaning out-of-date archives

Usage:
    fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

env.hosts = ['100.25.215.39', '34.203.38.206']


def clean_archives(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): Number of archives to keep.
            If number is 0 or 1, keeps only the most recent archive.
            If number is 2, keeps the most and second-most recent archives, and so on.
    """
    number = 1 if int(number) == 0 else int(number)

    # Delete local archives
    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Delete remote archives
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
