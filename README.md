# µspy deployment

<p align="center">
  <img width="417" height="300" src="proxmox/deployment.png">
</p>

This repo contains setup scripts and configuration files for deploying code on the agfalta jupyter server.

## Intro
The depolyment repository is organized as following:
```
deployment/
├─ dev / # Dev Container files
├─ jupyterhub/ # Jupyterhub files (Dockerfile, compose files, config, scripts)
├─ proxmox/ # Info about setting up PROXMOX Hypervisor
├─ docker/ # Files for uspy single user server (Dockerfile)
```

## Developing

For developing `uspy`, look at the documentation [here](dev/README.md). When you have tested your code changes in your local container, you can commit them to `uspy` and push to github. After that, you can update the version running on the server (next section).

## Update µSPY image

If you want to load a new version of µSPY execute the convenience script `deploy_uspy.sh` in deployment/jupyterhub. It expects the tag of the µSPY version as an Argument:

````
bash deploy_uspy.sh $VERSION
`````
It will atomatically pull the specified version, build the docker images, push to registry and restart jupyterhub to make changes effective.

## Adding users to Jupyterhub

Users can be added by running the script `add_user.sh` in deployment/jupyterhub. It expects accepts the name of the user as argument. If argument is given it will ask for the name. A new system user will be created with the name `jupyter-$NAME`. Jupyterhub is automatically restarted to make changes effective.

## Updating the Jupyterhub container itself

If changes are applied to `jupyterhub/jupyterhub_config.py` or the Jupyterhub `Dockerfile` jupyterhub needs to be rebuild. Run 
```
make rebuild
``` 
inside the `jupyterhub` folder. Restart Jupyterhub with `make restart`.

The Jupyterhub baseimage is the offical Jupyterhub image. The tag of the image corresponds to Jupyterhub version installed inside the image. Be aware, that the Jupyterhub version inside the Jupyterhub container must always match the version inside the `µspy` single-user containers. This is enforced by the `JUPYTERHUB_VERSION` argument in the `uspy Dockerfile`


## GPAW and quantum-espresso

Both packages are installed in the jupyterhub image. For more information see the [gpaw](https://wiki.fysik.dtu.dk/gpaw/index.html) and [QUANTUMESPRESSO](https://www.quantum-espresso.org/) websites.

The dependencies for both can be complicated, but QE is available through `apt`. For gpaw, the pseudopotential data needs to be downloaded via `gpaw install-data <dir>` (see [here](https://wiki.fysik.dtu.dk/gpaw/install.html)). In the single user JupyterHub containers, it is located in `$HOME/surfer-analysis/jupyter-data/gpaw_potentials`. In the current setup, `$HOME/surfer-analysis/` points to the surfer's mounted analysis directory (`/mnt/analysis`).

To set this up, you have to execute `jupyterhub/gpaw/install_gpaw.sh`. It places a `rc.py` in each user's `$HOME/.gpaw` directory so that gpaw actually knows the correct path.

