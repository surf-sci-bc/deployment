"""
This goes into
/opt/tljh/config/jupyterhub_config.d/
"""

from jupyter_client.localinterfaces import public_ips


def get_docker_tags(repo_name):
    try:
        import requests
        import json
    except ImportError:
        return ["latest"]
    req = requests.get(f"http://localhost:5000/v2/{repo_name}/tags/list")
    contents = json.loads(req.content)
    return contents["tags"]


c.JupyterHub.hub_ip = public_ips()[0]
c.JupyterHub.cleanup_servers = False
c.Spawner.default_url = "/lab"
c.SystemUserSpawner.host_homedir_format_string = "/home/jupyter-{username}"

c.JupyterHub.spawner_class = "dockerspawner.SystemUserSpawner"

c.DockerSpawner.allowed_images = dict(
    (tag, f"localhost:5000/agfalta_tools:{tag}")
    for tag in get_docker_tags("agfalta_tools")
)
c.DockerSpawner.pull_policy = "always"
c.DockerSpawner.remove = True
