# agfalta_tools deployment

<p align="center">
  <img width="417" height="300" src="proxmox/deployment.png">
</p>

This repo contains setup scripts and configuration files for deploying code on the agfalta jupyter server.


## Developing

For developing `agfalta_tools`, look at the documentation [here](dev/README.md). When you have tested your code changes in your local container, you can commit them to `agfalta_tools` and push to github. After that, you can update the version running on the server (next section).


## Updating the server

To use the newest `agfalta_tools` version on the jupyterhub, log into the jh server via ssh and clone this deployment repository there:

```sh
$ ssh xxx@jupyterhub.server
$ git clone git@github.com:surf-sci-bc/deployment.git
```

Then, go into the deployment directory. To build a new docker container from the most recent `agfalta_tools` commit and push it for use in Jupyterhub, just use the make target:

```sh
$ cd deployment
$ make update
```


## Updating the Jupyterhub container itself

If you want to apply changes to the JH config, first follow the instructions from the last paragraph except for the last command. Then, do `$ make jh-restart` instead of update. This rebuilds the JH container, restarts it and the docker registry.


