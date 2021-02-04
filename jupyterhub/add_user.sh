#!/bin/bash
echo "Creating User jupyter-$1"
adduser -q --gecos "" --disabled-password jupyter-$1

echo "Remember to restart Jupyterhub Container by:"
echo "docker-compose restart jupyterhub"