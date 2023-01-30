#!/bin/bash
if [[ -z $* ]] ; then
    echo 'No user name was given.'
    echo 'Please provide user name:'
    read NAME
else
    NAME=$1
fi
echo "Creating User jupyter-$NAME"
adduser -q --gecos "" --disabled-password jupyter-$1
echo "Restarting jupyterhub to load new user"
docker-compose restart jupyterhub