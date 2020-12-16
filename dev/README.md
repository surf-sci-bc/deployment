# Development

Use this to do development in a (local) docker container that uses an editable install of ```agfalta_tools``` that is mounted from your project folder.

## Preparation

Get a working Docker installation. Refer to the install guidelines in [this README](../deployment/tljh/README.md).

Clone this `deployment` repository and `cd` into it:

```
$ git clone git@github.com:surf-sci-bc/deployment.git
$ cd deployment/
```

## Build the docker image

Use either one of the following subsections, not both.

### Automatically download a new copy of `agfalta_tools`

Do this from the `deployment` directory:

```
$ make dev-build
```

This creates a new git repo copy of `agfalta_tools` in `deployment/dev/` and then builds a docker container with that version installed. You can edit it there and changes are reflected directly in your running jupyterlab (see [below](#set-sails)).

### Use an existing copy of `agfalta_tools`

If you have not done this yet, clone the `agfalta_tools` repository to your projects folder

```
$ cd /path/to/projects
$ git clone git@github.com:surf-sci-bc/agfalta_tools.git
```

To make the image smaller, copy `deployment/dev/.dockerignore` to your `agfalta_tools` folder because that will be the build context of the docker image. You can adapt it to your pleasure, but
it should at least contain the `.git` folder.

```
$ cp .dockerignore /path/to/projects/agfalta_tools/.dockerignore
```

Now you can build the image (from the `deployment` directory):

```
$ make REPO_DIR=/path/to/projects/agfalta_tools dev-build
```

This will take a short while, but only has to be performed once unless the `Dockerfile` is changed or new requirements have to be installed. 

_Note:_ this will write your `REPO_DIR` path into the file `deployment/dev/repo_location.txt` to use it in all further commands. If you wish to change the `agfalta_tools` location, either repeat above command with another path or delete the `repo_location.txt` file. If the path will stay the same, you can omit that parameter and just write `$ make dev-build` from now on.


## Set sails

Run the container (from the `deployment` directory) with:

```
$ make dev-run
```

You can now access the container by the link that is given in the terminal. `agfalta_tools` is mounted from the projects folder, so changes to `agfalta_tools` are directly affecting the development environment inside the container and vice versa.

_Note:_ If you want to use JupyterLab instead of Jupyter notebook, change the last part of the URL from `tree` to `lab`.


## Additional variables

For the relevant commands, some values can be changed from the command line (like with `REPO_DIR`):

* `IMAGE_NAME`: The name of the docker image. Defaults to `agfalta_tools-dev` (relevant for build and run)
* `CONT_NAME`: Name of the container that the run target creates (it is destroyed automatically after stopping). Defaults to `agfalta_tools_devJL`
* `VERSION`: Version of `agfalta` as a git reference. Defaults to `HEAD`