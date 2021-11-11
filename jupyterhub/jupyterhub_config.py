# pylint: disable=missing-docstring
# pylint: disable=import-error

# TODO:
# - Parse passwd file for users
# - Add another option to image whitelist, if only one is present
# - Later: Use LocalFirstUseAuthenticator again

import sys
import pwd
import os

import requests
import json

from dockerspawner import SystemUserSpawner
from firstuseauthenticator import FirstUseAuthenticator
# from jupyterhub.auth import LocalAuthenticator
# from jupyter_client.localinterfaces import public_ips
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

# class DummyUser:
#     # pylint: disable=too-few-public-methods
#     def __init__(self, user):
#         self.name = convert_username(user.name)

# class LocalFirstUseAuthenticator(FirstUseAuthenticator, LocalAuthenticator):
#     def system_user_exists(self, user):
#         user = DummyUser(user)
#         return super().system_user_exists(user)

#     def add_system_user(self, user):
#         user = DummyUser(user)
#         self.log.info(user)
#         return super().add_system_user(user)

def get_docker_repos():
    req = requests.get(f"http://registry:5000/v2/_catalog")
    contents = json.loads(req.content)
    repos = contents["repositories"]
    # put uspy first if it is there
    if "uspy" in repos:
        repos.remove("uspy")
        repos.insert(0, "uspy")
    return repos

def get_docker_tags(repo_name):
    req = requests.get(f"http://registry:5000/v2/{repo_name}/tags/list")
    contents = json.loads(req.content)
    tags = contents["tags"]
    def semversort(s):
        try:
            return list(map(int, s.split(".")))
        except ValueError:
            return list(map(ord, s))
    tags.sort(key=semversort, reverse=True)
    return tags

def get_user_names():
    directory_contents = os.listdir("/home/")
    # Check if home directory exists with jupyter prefix
    return [item.split("-")[1] for item in directory_contents if os.path.isdir("/home/"+item) and "jupyter-" in item]



# pylint: disable=undefined-variable
### General config
c.JupyterHub.hub_ip = ''
network_name = os.environ['DOCKER_NETWORK_NAME']
c.JupyterHub.cleanup_servers = False
c.JupyterHub.services = [{
    "name": "cull-idle", "admin": True, "command": [
        sys.executable, "-m", "jupyterhub_idle_culler",
        "--timeout=86400", "--cull-every=60",
        "--max-age=604800", "--concurrency=10",
    ]
}]

### Spawner config
c.JupyterHub.spawner_class = MyDockerSpawner
c.DockerSpawner.network_name = network_name
c.Spawner.default_url = "/lab"
c.SystemUserSpawner.host_homedir_format_string = "/home/jupyter-{username}"
c.SystemUserSpawner.image_homedir_format_string = "/home/jupyter-{username}"
c.SystemUserSpawner.environment = {"NB_UMASK": "0022"}
c.SystemUserSpawner.run_as_root = True

repos = get_docker_repos()
allowed_images = dict()
for repo in repos:
    for tag in get_docker_tags(repo):
        allowed_images[f"{repo}:{tag}"] = f"localhost:5000/{repo}:{tag}"

c.MyDockerSpawner.allowed_images = allowed_images

c.DockerSpawner.volumes = {
    "/home/agfalta/public":           {"bind": "/home/jupyter-{username}/public", "mode": "rw"},
    "/mnt/analysis/jupyter-labbooks": {"bind": "/home/jupyter-{username}/labbooks", "mode": "rw"},
    "/mnt/analysis/jupyter-examples": {"bind": "/home/jupyter-{username}/examples", "mode": "ro"},
    "/mnt/analysis":                  {"bind": "/home/jupyter-{username}/surfer-analysis", "mode": "rw"},
    "/mnt/data":                      {"bind": "/home/jupyter-{username}/data", "mode": "ro"},
}
c.DockerSpawner.pull_policy = "always"
c.DockerSpawner.remove = True


### Authenticator config
c.JupyterHub.authenticator_class = FirstUseAuthenticator #LocalFirstUseAuthenticator
FirstUseAuthenticator.dbm_path = "/srv/jupyterhub/password/"
c.FirstUseAuthenticator.create_users = False
c.LocalAuthenticator.create_system_users = False
c.Authenticator.admin_users = {'admin'}
c.Authenticator.allowed_users = set(name for name in get_user_names())


### Proxy config
c.JupyterHub.proxy_class = TraefikTomlProxy
c.TraefikTomlProxy.traefik_api_username = "admin"
c.TraefikTomlProxy.traefik_api_password = "admin"
c.TraefikTomlProxy.traefik_log_level = "INFO"
