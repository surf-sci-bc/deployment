# Deploy fully containerized Jupyterhub with Docker

### This is the recommended deployment procedure

By Jupyterhub inside a docker container, it is possible to get an almost stateless configuration, that can be deployed and updated with only a few commands.

## Install Docker
Because TLJH is supposed to run the single-user servers inside docker containers, docker needs to be installed on the host
````
sudo apt update && sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update && sudo apt install -y docker-ce
````
This adds the docker repository to apt, adds the key and installs the docker community edition.

### Add user to docker group
To run docker without using sudo, the user has to added to the docker group (which has to be created first when not already present). Note granting a user sudoless docker permission is equivalent to granting root permission to this user.
````
sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker
````
The installation can be checked by:
````
 docker run hello-world
````
which should yield a hello world message.

## Install docker-compose

Execute the following commands.

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Create a Notebook user

Because the Hub is running inside container using its own user managment, it is difficult to create users on the host from inside the container.
However, by mounting ```/etc/passwd/``` in the container, the Hub is aware of the hosts users and is able to spawn the lab-containers with the right permissions. This also means that the lab-users have to be already existant on host at hub startup. Using the ```add_user``` script, creates the users with the neccessary configuration

```
./add_user.sh <user-name-in-hub>
```
The user will be created as ```jupyter-<user-name-in-hub >```. Still for the hub ```<user-name-in-hub>``` is neccessary as normalisation of the username is done during authentication. The allowed users are determined by the presence of ```jupyter-*```-folder in ```/home/``` at startup of the hub. After creation of a new user the hub has to be restarted. By
````
docker-compose restart
````

## Build Jupyterlab Image

First, install [docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) according to their doc (just click the links).

Build the image for the jupyterlab container within the work directory:

```
docker build -t agfalta/jupyterhub .
```

## Start Jupyterhub

Jupyterhub is started by using docker-compose in the same folder as the ```docker-compose.yaml``` file:

```
sudo docker-compose up -d
```

This file takes care of all neccessary configuraiton, including networking, volumes and bindmounts. Next to the Jupyterhub it also deploys a registry container. That the agfalta_tools images can be pushed to, so they are spawnable by the hub.  
  
The Hub utilizes the FirstUseAuthenicator for Authentication. This means, that the password is set while logging in for the first time. The passwords and the registry data is persistent.

## Push to registry

Push an image to the registry by tagging it with the registry ```ip``` and ```port```. Choose the ```<TAG>``` accoarding to the ```agfalta_tools``` version beeing built.

```
cd deployment
make docker
```

Alternativly, use the
```
make docker
```
in the parent direcotry. This takes care of everything.

## Have fun.

Now it sould be possible to spawn a ```agfalta_tools``` container, with a authenticated user.
