ARG BASE_CONTAINER=jupyter/minimal-notebook:09fb66007615
# History
# 07.12.2020 | 399cbb986c6b
# 29.01.2021 | 5cb007f03275
# 27.04.2021 | 584f43f06586
# 07.05.2021 | 09fb66007615

FROM $BASE_CONTAINER

# Jupyterhub version has to match version inside the jupyterhub dockerfile
ARG JUPYTERHUB_VERSION=1.4.0

USER root

# ffmpeg for matplotlib anim & dvipng+cm-super for latex labels
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg dvipng cm-super quantum-espresso && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_UID

RUN conda install --quiet --yes \
    'gpaw=21.1.*' \
    'ipywidgets=7.6.*' \
    'ipympl=0.7.*'\
    'jupyterhub='$JUPYTERHUB_VERSION \
    'matplotlib-base=3.4.*' \
    && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME="/home/${NB_USER}/.cache/"

RUN MPLBACKEND=Agg python3 -c "import matplotlib.pyplot" && \
    fix-permissions "/home/${NB_USER}"

#-------------------------
# Make changes below this line to avoid cache busting

WORKDIR $HOME

# currently relies on agfalta_tools being in the same directory as the Dockerfile
COPY --chown=${NB_UID}:${NB_GID} . agfalta_tools

RUN python3 -m pip install -e agfalta_tools/. && \
    rm -rf agfalta_tools/* && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

