"""
This goes into
/opt/tljh/config/jupyterhub_config.d/
"""
# pylint: disable=missing-docstring
# pylint: disable=import-error

import sys
import pwd
from dockerspawner import SystemUserSpawner
from firstuseauthenticator import FirstUseAuthenticator
from jupyterhub.auth import LocalAuthenticator

from jupyter_client.localinterfaces import public_ips
from tornado import gen


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


def get_docker_tags(repo_name):
    try:
        import requests
        import json
    except ImportError:
        return ["latest"]
    req = requests.get(f"http://localhost:5000/v2/{repo_name}/tags/list")
    contents = json.loads(req.content)
    return contents["tags"]

# pylint: disable=undefined-variable
### General config
c.JupyterHub.hub_ip = public_ips()[0]
c.JupyterHub.cleanup_servers = False
c.JupyterHub.services = [{
    "name": "cull-idle", "admin": True, "command": [
        sys.executable, "-m", "jupyterhub_idle_culler",
        "--timeout=3600", "--cull-every=60",
        "--max-age=0", "--concurrency=10",
    ]
}]

### Spawner config
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
c.JupyterHub.authenticator_class = LocalFirstUseAuthenticator
c.FirstUseAuthenticator.create_users = False
c.LocalAuthenticator.create_system_users = True
