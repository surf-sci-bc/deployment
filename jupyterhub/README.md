# Deploy Jupyterhub with docker

Deploying Jupyterhub inside a docker container, it is possible to get an almost stateless configuration, that can be deployed and updated with only a few commands.

## Create a Notebook user

Because the Hub is running inside container using its own user managment, it is difficult to create users on the host from inside the container.
However, by mounting ```/etc/passwd/``` in the container, the Hub is aware of the hosts users, is able to spawn the lab-containers with the right permissions. This means that the lab-users have to be already existant on host at hub startup. Using the ```add_user``` script, creates the users with the neccessary configuration

```
./add_user.sh <user-name-in-hub>
```
The user will be created as ```jupyter-<user-name-in-hub >```. Still for the hub ```<user-name-in-hub>``` is neccessary as normalisation of the username is done during authentication. The allowed users are determined by the presence of ```jupyter-*```-folder in ```/home/``` at startup of the hub. After creation of a new user the hub has to be restarted.

## Build Jupyterlab Image

Build the image for the jupyterlab container within the work directory:
````
docker build -t agfalta/jupyterhub .
````

## Start Jupyterhub

Jupyterhub is started by using docker-compose in the same folder as the ```docker-compose.yaml``` file:
```
sudo docker-compose -d up
```
This file takes care of all neccessary configuraiton, including networking, volumes and bindmounts. Next to the Jupyterhub it also deploys a registry container. That the agfalta_tools images can be pushed to, so they are spawnable by the hub.  
  
The Hub utilizes the FirstUseAuthenicator for Authentication. This means, that the password is set while logging in for the first time. The passwords and the registry data is persistent.

## Push to registry

Push an image to the registry by tagging it with the registry ```ip``` and ```port```. Choose the ```<TAG>``` accoarding to the ```agfalta_tools``` version beeing built.
```
cd deployment/docker
docker build -t localhost:5000/agfalta_tools:<TAG> .
docker push localhost:5000/agfalta_tools:<TAG>
```

## Have fun.

Now it sould be possible to spawn a ```agfalta_tools``` container, with a authenticated user.