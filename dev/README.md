# Development

Following this approach development is done by creating a docker container, that
uses a editable install of the ```agfalta_tools```, while mounting the ```agfalta_tools```
folder from the hosts project folder.

## Preparation

Get a working Docker installation. Refer to the install guidelines in ```deployment/tljh/README```.

Clone the ```agfalta_tools``` repository to your projects folder
```
cd /path/to/projects
git clone git@github.com:surf-sci-bc/agfalta_tools.git
```

To develop the ```agfalta_tools``` package clone the ```deployment``` repository
or download the ```deployment/dev``` to another directory:

```
cd /other/directory (eg. parent directory of agfalta_tools)
git clone git@github.com:surf-sci-bc/deployment.git
cd deployment/dev/
```
Copy ```.dockerignore``` to your ```agfalta_tools``` folder, as the a```agfalta_tools``` will
be the build context of the docker image. You can adapt it to your pleasure, but
it should at least contain the ```.git``` folder.

```
cp .dockerignore /path/to/projects/agfalta_tools/.dockerignore
```
You can also copy the Dockerfile and Makefile to the same directory. Then you
have to add ```Dockerfile``` and ```Makefile``` to .dockerignore  

Edit the Makefile and change ```REPO_DIR``` to your agfalta_tools folder. If you copied
```Dockerfile```, ```Makefile``` and ```.dockerignore``` you can set
```REPO_DIR = .```

## Set sails

Build the image by
```
make build
```
This will take a while, but only has to be performed once unless the ```Dockerfile``` is changed or new requirements have to be installed.

Run the container by
```
make run
```
You can now access the container by the link that is given in the terminal. The ```agfalta_tools``` are mounted form the projects folder, so changes to the ```agfalta_tools``` are directly affecting the development environment inside the container and vice versa.
