"""
This goes into
/opt/tljh/config/jupyterhub_config.d/
"""
# pylint: disable=missing-docstring
# pylint: disable=import-error

import sys
import pwd
import os
import re

from dockerspawner import SystemUserSpawner
from firstuseauthenticator import FirstUseAuthenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.auth import PAMAuthenticator


from jupyter_client.localinterfaces import public_ips
from tornado import gen

from jupyterhub_traefik_proxy import TraefikTomlProxy

def convert_username(user_name):
    return f"jupyter-{user_name}"

class MyDockerSpawner(SystemUserSpawner):
    def get_env(self):
        env = super().get_env()
        user_name = convert_username(self.user.name)
        env.update(dict(USER=user_name, NB_USER=user_name))
        return env

    def _user_id_default(self):
        return pwd.getpwnam(convert_username(self.user.name)).pw_uid

    def _group_id_default(self):
        return pwd.getpwnam(convert_username(self.user.name)).pw_gid

    @gen.coroutine
    def pull_image(self, image):
        """
        For some reason this is neccesarry. Dont ask me why. It just overrides
        the pull always behavor of dockerspawner but it seems to be neccessary.
        """
        if ':' in image.split("/")[-1]:
            # rsplit splits from right to left, allowing to have a custom image repo with port
            repo, tag = image.rsplit(':', 1)
        else:
            repo = image
            tag = 'latest'
        self.log.info(f"Pulling image {repo}:{tag}...")
        yield self.docker('pull', repo, tag)
        return
    #@gen.coroutine
    #def get_ip_and_port(self):
    #    return self.host_ip, self.port
    

class DummyUser:
    # pylint: disable=too-few-public-methods
    def __init__(self, user):
        self.name = convert_username(user.name)

class LocalFirstUseAuthenticator(FirstUseAuthenticator, LocalAuthenticator):
    def system_user_exists(self, user):
        user = DummyUser(user)
        return super().system_user_exists(user)

    def add_system_user(self, user):
        user = DummyUser(user)
        self.log.info(user)
        return super().add_system_user(user)

class MyPAMAuthenticator(PAMAuthenticator):
    def normalize_username(self, username):
        self.log.info(convert_username(username))
        return convert_username(username)
        #return f"jupyter-{username}"


def get_docker_tags(repo_name):
    try:
        import requests
        import json
    except ImportError:
        return ["latest"]
    req = requests.get(f"http://registry:5000/v2/{repo_name}/tags/list")
    contents = json.loads(req.content)
    return contents["tags"]

def get_user_names():
    directory_contents = os.listdir("/home/")    
    # Check if home directory exists with jupyter prefix
    return [item.split("-")[1] for item in directory_contents if os.path.isdir("/home/"+item) and "jupyter-" in item]


# pylint: disable=undefined-variable
### General config
#c.JupyterHub.hub_ip = public_ips()[0]
#c.JupyterHub.hub_ip = '0.0.0.0'  # listen on all interfaces
#c.JupyterHub.hub_ip = '10.0.1.4'
c.JupyterHub.hub_ip = ''
#c.JupyterHub.hub_connect_ip = 'jupyterhub'
#c.DockerSpawner_host.use_internal_ip = False
#c.JupyterHub.ip = ''
c.JupyterHub.cleanup_servers = False
c.JupyterHub.services = [{
    "name": "cull-idle", "admin": True, "command": [
        sys.executable, "-m", "jupyterhub_idle_culler",
        "--timeout=3600", "--cull-every=60",
        "--max-age=0", "--concurrency=10",
    ]
}]

### Spawner config
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.network_name = network_name

c.JupyterHub.spawner_class = MyDockerSpawner
c.Spawner.default_url = "/lab"
c.SystemUserSpawner.host_homedir_format_string = "/home/jupyter-{username}"
c.SystemUserSpawner.image_homedir_format_string = "/home/jupyter-{username}"
c.SystemUserSpawner.environment = {"NB_UMASK": "0022"}

c.DockerSpawner.image_whitelist = dict(
    (tag, f"localhost:5000/agfalta_tools:{tag}")
    for tag in get_docker_tags("agfalta_tools")
)
c.DockerSpawner.volumes = {
    "/home/agfalta/public": {"bind": "/home/jupyter-{username}/public", "mode": "rw"},
    "/mnt/analysis/jupyter-labbooks": {"bind": "/home/jupyter-{username}/labbooks", "mode": "rw"},
    "/mnt/analysis/demos": {"bind": "/home/jupyter-{username}/demos", "mode": "rw"},
    "/mnt/data": {"bind": "/home/jupyter-{username}/data", "mode": "ro"}
}
c.DockerSpawner.pull_policy = "always"
c.DockerSpawner.remove = True

### Authenticator config
c.JupyterHub.authenticator_class = FirstUseAuthenticator #MyLocalAuthenticator #PAMAuthenticator #LocalAuthenticator #FirstUseAuthenticator
FirstUseAuthenticator.dbm_path = "/srv/jupyterhub/password/"
c.FirstUseAuthenticator.create_users = False
c.LocalAuthenticator.create_system_users = False

### Proxy config
c.JupyterHub.proxy_class = TraefikTomlProxy
c.TraefikTomlProxy.traefik_api_username = "admin"
c.TraefikTomlProxy.traefik_api_password = "admin"
c.TraefikTomlProxy.traefik_api_url = "http://jupyterhub:8099"
c.TraefikTomlProxy.traefik_log_level = "INFO"

### Admin User
c.Authenticator.admin_users = {'admin'}

### User
c.Authenticator.allowed_users = set(name for name in get_user_names())

