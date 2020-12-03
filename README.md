# agfalta_tools deployment

This repo contains setup scripts and configuration files for deploying code on the agfalta jupyter server.

## TLJH

Refer to that [README](tljh/README.md). To apply the TLJH configuration file, you can also do this command from here:

```sh
sudo make tljh-config
```


### Creating the docker image

To build a new docker container from the most recent `agfalta_tools` commit and push it for use in TLJH, do:

```sh
make update
```
