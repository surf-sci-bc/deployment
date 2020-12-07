ARG BASE_CONTAINER=jupyter/minimal-notebook:399cbb986c6b
# History
# 07.12.2020 | 399cbb986c6b
#

FROM $BASE_CONTAINER

ARG JUPYTERHUB_VERSION=1.1.0
#RUN python3 -m pip install --upgrade --no-cache-dir jupyterhub==$JUPYTERHUB_VERSION

USER root

# ffmpeg for matplotlib anim & dvipng+cm-super for latex labels
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg dvipng cm-super && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_UID

RUN conda install --quiet --yes \
    'ipywidgets=7.5.*' \
    'ipympl=0.5.*'\
    'jupyterhub='$JUPYTERHUB_VERSION \
    'matplotlib-base=3.3.*' \
    && \
    conda clean --all -f -y && \
    # Check this URL for most recent compatibilities
    # https://github.com/jupyter-widgets/ipywidgets/tree/master/packages/jupyterlab-manager
    jupyter labextension install @jupyter-widgets/jupyterlab-manager@^2.0.0 --no-build && \
    jupyter labextension install jupyter-matplotlib@^0.7.2 --no-build && \
    jupyter lab build -y && \
    jupyter lab clean -y && \
    npm cache clean --force && \
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    rm -rf "/home/${NB_USER}/.node-gyp" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME="/home/${NB_USER}/.cache/"

RUN MPLBACKEND=Agg python3 -c "import matplotlib.pyplot" && \
    fix-permissions "/home/${NB_USER}"

#-------------------------
# Make changes below this line to avoid cache busting

# currently relies on agfalta_tools being in the same directory as the Dockerfile
COPY --chown=${NB_UID}:${NB_GID} agfalta_tools /tmp/agfalta_tools

RUN python3 -m pip install --no-cache-dir /tmp/agfalta_tools/. && \
    rm -rf /tmp/agfalta_tools && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

WORKDIR $HOME
