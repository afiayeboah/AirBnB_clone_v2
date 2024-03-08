#!/usr/bin/python3
"""
Fabric script for creating and distributing a compressed archive to web servers

Usage:
    Execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# Define remote hosts
env.hosts = [' 34.203.38.206', '100.25.215.39']


def create_compressed_archive():
    """
    Create a compressed archive of the web_static directory

    Returns:
        str: Path of the created archive if successful, otherwise None
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print("Error creating compressed archive:", e)
        return None


def deploy():
    """
    Create a compressed archive of the web_static directory and deploy it to web servers

    Returns:
        bool: True if deployment is successful, False otherwise
    """
    archive_path = create_compressed_archive()
    if archive_path is None:
        print("Failed to create compressed archive.")
        return False

    if not exists(archive_path):
        print("Archive does not exist:", archive_path)
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_extension = file_name.split(".")[0]
        remote_path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(remote_path, no_extension))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, remote_path, no_extension))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(remote_path, no_extension))
        run('rm -rf {}{}/web_static'.format(remote_path, no_extension))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(remote_path, no_extension))
        return True
    except Exception as e:
        print("Error deploying archive:", e)
        return False
