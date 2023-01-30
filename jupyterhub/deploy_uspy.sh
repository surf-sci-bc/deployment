#!/bin/bash
set -e

uspy_docker_path="../docker/"

echo "Bring up Registry."
docker-compose up -d registry
echo "Pull latest uspy"
git -C $uspy_docker_path/uspy pull || git clone https://github.com/surf-sci-bc/uspy.git $uspy_docker_path/uspy
echo "Checkout Tag $1"
git -C $uspy_docker_path/uspy checkout $1
echo "Done."
echo "Building Docker image:"
docker build -t localhost:5000/uspy:latest -t localhost:5000/uspy:$1 $uspy_docker_path
echo "Push Images:"
docker push localhost:5000/uspy:latest
docker push localhost:5000/uspy:$1
echo "Restart Jupyterhub."
docker-compose restart
echo "Done."