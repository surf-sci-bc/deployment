# Setting up TLJH on Proxmox

## Preparation
see https://tljh.jupyter.org/en/latest/install/custom-server.html for reference. First make sure the necessary packages are installed:

````
sudo apt install python3 python3-dev git curl
````
Now that you have git you can already clone the git repository. It seems to be good to do this first, because the TLJH installer seems to mess up some permissions when it runs git first. In order to get the agfalta repository refer to the ````README.md```` of the repository.

For now:
````
cd ~
git clone https://github.com/surf-sci-bc/agfalta_tools.git
````
You need access to the private repository to clone it. Now that you have done this


## Install The Littlest Jupyterhub
see https://tljh.jupyter.org/en/latest/install/custom-server.html for reference.

Now everything is prepared to install TLJH

````
curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
  | sudo python3 - \
    --admin admin
````
This takes approx. 3-5 min.  

If you type this over ssh or terminal note that the "enter password" request might be written between the output of the ````curl```` function. So if the installer seems frozen check if the password needs to be given.

After the installation is finished open http://\<ip-of-hub\> and log in with username ````admin````. The password will be set upon first use. Remeber the password.

Check that a home directory named ````jupyter-admin```` has been created.

## Install Docker
Because TLJH is supposed to run the single-user serveres inside docker containers, docker needs to be installed on the host
````
sudo apt update && sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update && sudo apt install -y docker-ce
````
This adds the docker repository to apt, adds the key and installs the docker community edition.

### Add user to docker group
To run docker without using sudo, the user has to added to the docker group (which has to be created first when not already present)
````
sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker
````
The installation can be checked by:
````
 docker run hello-world
````
which should yield a hello world message

### Set up docker registry
In order for Jupyterhub to find the docker image to run a container a registry has to set up, where the images are pushed to. This creates a registry-server which listens to ````port 5000```` of ````localhost````. It is only available from ````localhost```` which should be no problem for this use case. When exposing to outside of ````localhost```` additional security measures have to be taken!
````
docker run -d -p 5000:5000 --name registry --restart=always -e REGISTRY_STORAGE_DELETE_ENABLED=true registry:2
````

## Install Dockerspawner
Dockerspawner is used for spawning single user servers inside docker containers. It has to be installed to the virtual environment of TLJH.

````
sudo -E /opt/tljh/hub/bin/python3 -m pip install dockerspawner jupyter_client
````

## Configuration

Put the config file into the right directory (assumes you are in this repo's root):

```
$ sudo cp tljh/jupyterhub_config.py /opt/tljh/config/jupyterhub_config.d
$ sudo tljh-config reload
```
Reload the configuration

````
sudo tljh-config reload
````
## Mounting the surfer data file

Open fstab by `sudo nano /etc/fstab`. Then add this line:

```
# Add to /etc/fstab
//192.168.2.99/data   /home/agfalta/data    cifs    credentials=/home/agfalta/.credentials,auto,ro,mfsymlinks   0   0
```

You need to have the credentials of the data servers samba user in the above mentioned file in this form:
```
# /home/agfalta/.credentials
user=xxx
password=xxx
```

Also install cifs and finally mount the data volume:

```sh
$ sudo apt install cifs-utils
$ sudo mount -a
```
