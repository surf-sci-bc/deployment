# pylint: disable=missing-docstring
# pylint: disable=import-error



import sys
import pwd
import os

import requests
import json

from dockerspawner import SystemUserSpawner
from firstuseauthenticator import FirstUseAuthenticator
from tornado import gen
#from jupyterhub_traefik_proxy import TraefikTomlProxy

# Import volume configuration
try:
    from volumes_config import VOLUMES
except ImportError:
    print("Warning: volumes_config.py not found. Using empty volume configuration.")
    VOLUMES = {}


def convert_username(user_name):
    return f"jupyter-{user_name}"


class MyDockerSpawner(SystemUserSpawner):
    def get_env(self):
        env = super().get_env()
        user_name = convert_username(self.user.name)
        env.update(dict(USER=user_name, NB_USER=user_name))
        return env
    
    def get_docker_images(self):
        response = requests.get("http://registry:5000/v2/_catalog")
        response.raise_for_status()
        repos = response.json().get('repositories', [])
        if "uspy" in repos:
            repos.remove("uspy")
            repos.insert(0, "uspy")

        return repos
        
    def get_image_tags(self, image):
        url = f"http://registry:5000/v2/{image}/tags/list"
        response = requests.get(url)
        response.raise_for_status()
        tags = response.json().get('tags', [])
        if "latest" in tags:
            tags.remove("latest")
            tags.insert(0, "latest")

        return tags
      
    def get_images_with_tags(self):
        repositories = self.get_docker_images()
        image_tag_map = {}

        for image in repositories:
            tags =self.get_image_tags(image)
            image_tag_map[image] = tags

        return image_tag_map

    def _user_id_default(self):
        return pwd.getpwnam(convert_username(self.user.name)).pw_uid

    def _group_id_default(self):
        return pwd.getpwnam(convert_username(self.user.name)).pw_gid

    def _options_form_default(self):
        # Hardcoded image names and tags. Replace with dynamic logic if necessary
        images = self.get_images_with_tags()

        form_html = """
        <style>
            /* Base font and layout adjustments to match JupyterHub style */
            body, .form-container, .spawner-form {{
                font-family: "Helvetica Neue", Arial, sans-serif;
                color: #333;
            }}

            /* Form container to match the login box */
            .spawner-form {{
                background-color: #fff;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 20px;
                max-width: 400px;
                margin: 40px auto;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}

            /* Header bar similar to JupyterHub's orangecd  sign-in bar */
            .spawner-header {{
                background-color: #f57c00;
                padding: 10px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                color: white;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 20px;
            }}

            /* Input fields matching JupyterHub login inputs */
            .spawner-form label {{
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 8px;
                display: block;
            }}

            .spawner-form select {{
                width: 100%;
                font-size: 16px;
                padding: 12px;
                margin-bottom: 20px;
                border-radius: 8px;
                border: 1px solid #ccc;
                background-color: #f9f9f9;
                box-sizing: border-box;
                height: 45px; /* To make dropdown taller */
            }}

            .spawner-form select:focus {{
                outline: none;
                border-color: #a0a0a0;
                background-color: #fff;
            }}

            /* Styling the button to match the orange sign-in button */
            .spawner-form .submit-btn {{
                background-color: #f57c00;
                color: white;
                padding: 12px;
                font-size: 16px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                width: 100%;
            }}

            .spawner-form .submit-btn:hover {{
                background-color: #e57300;
            }}

            .spawner-form .description {{
                font-size: 12px;
                color: #666;
                margin-bottom: 10px;
            }}

            /* Center the form on the page */
            .form-container {{
                display: flex;
                justify-content: center;
                align-items: start;
                min-height: 20vh;
            }}
        </style>

        <div class="form-container">
            <div class="spawner-form">
                <div class="spawner-header">Select Environment</div>
                
                <label for="image">Select your desired image:</label>
                <select id="image" name="image" size="1" onchange="updateTags()">
                {image_options}
                </select>
                <div class="description">Choose the base environment or software stack you'd like to use.</div>

                <label for="tag">Select your desired tag (version):</label>
                <select id="tag" name="tag" size="1">
                </select>
                <div class="description">Pick the version of the selected environment (latest or specific).</div>

                <!--<button class="submit-btn" type="submit">Start Environment</button>-->
            </div>
        </div>

        <script type="text/Javascript">
        function updateTags() {{
            var images = {images};
            var imageSelect = document.getElementById("image");
            var tagSelect = document.getElementById("tag");

            var selectedImage = imageSelect.options[imageSelect.selectedIndex].value;
            tagSelect.innerHTML = "";

            images[selectedImage].forEach(function(tag) {{
                var opt = document.createElement('option');
                opt.value = tag;
                opt.innerHTML = tag;
                tagSelect.appendChild(opt);
            }});
        }}

        // Update the tags dropdown when the page loads
        document.addEventListener("DOMContentLoaded", function() {{
            updateTags();
        }});
        </script>
        """


        image_options = '\n'.join([f'<option value="{image}">{image}</option>' for image in images.keys()])

        return form_html.format(images=images, image_options=image_options)

    def options_from_form(self, formdata):
        # Extract the selected image and tag from the form data
        selected_image = formdata.get('image', [''])[0]  # Extract the image name
        selected_tag = formdata.get('tag', ['test'])[0]      # Extract the tag

        # Combine image and tag to form the full container image (e.g., uspy:v1.0)
        container_image = f"{selected_image}:{selected_tag}"

        # Log or print for debugging (optional)
        print(f"Selected image: {selected_image}")
        print(f"Selected tag: {selected_tag}")
        print(f"Full container image: {container_image}")

        # Set the full container image for spawning
        #self.image = container_image

        # Return the selected options for later use
        return {
            'image': container_image,
            'selected_image': selected_image,
            'selected_tag': selected_tag
        }
    
c.JupyterHub.log_level = 'DEBUG'
c.Spawner.debug = True  # Enable detailed logging for the spawner

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

### Idle Culler Config
c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
        ],
        "services": ["jupyterhub-idle-culler-service"],
    }
]

c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=86400",
        ],
    }
]

### Spawner config
c.JupyterHub.spawner_class = MyDockerSpawner
c.DockerSpawner.network_name = network_name
c.SystemUserSpawner.host_homedir_format_string = "/home/jupyter-{username}"
c.SystemUserSpawner.image_homedir_format_string = "/home/jupyter-{username}"
c.SystemUserSpawner.environment = {"NB_UMASK": "0022"}
c.SystemUserSpawner.run_as_root = True

repos = get_docker_repos()
allowed_images = dict()
for repo in repos:
    for tag in get_docker_tags(repo):
        allowed_images[f"{repo}:{tag}"] = f"localhost:5000/{repo}:{tag}"

# specfiying the images explicilty is for some reason neccessary, maybe because of 'localhost'
c.MyDockerSpawner.allowed_images = allowed_images

# Set volumes from imported configuration
c.MyDockerSpawner.volumes = VOLUMES
c.MyDockerSpawner.pull_policy = "always"
c.MyDockerSpawner.remove = True

### Authenticator config
c.JupyterHub.authenticator_class = FirstUseAuthenticator
FirstUseAuthenticator.dbm_path = "/srv/jupyterhub/password/"
c.FirstUseAuthenticator.create_users = False
c.LocalAuthenticator.create_system_users = False
c.Authenticator.admin_users = {'admin'}
c.Authenticator.allowed_users = set(name for name in get_user_names())
#c.Authenticator.allowed_users = ("Lars",) ## CHANGE THIS
### Proxy config
c.JupyterHub.proxy_class = "traefik_file"#TraefikTomlProxy
c.TraefikTomlProxy.traefik_api_username = "admin"
c.TraefikTomlProxy.traefik_api_password = "admin"
c.TraefikTomlProxy.traefik_log_level = "INFO"