"""
This goes into
/opt/tljh/config/jupyterhub_config.d/
"""
from jupyter_client.localinterfaces import public_ips
from systemuserspawner import SystemUserSpawner
from tornado import gen, web


class MyDockerSpawner(SystemUserSpawner):
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
        self.log.info("This is a custom image puller")
        self.log.info("Repo: %s"%repo)
        self.log.info("Tag: %s"%tag)
        yield self.docker('pull', repo, tag)
        return


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

# c.JupyterHub.spawner_class = "dockerspawner.SystemUserSpawner"
c.JupyterHub.spawner_class = MyDockerSpawner

c.DockerSpawner.image_whitelist = dict(
    (tag, f"localhost:5000/agfalta_tools:{tag}")
    for tag in get_docker_tags("agfalta_tools")
)
c.DockerSpawner.pull_policy = "always"
c.DockerSpawner.remove = True
