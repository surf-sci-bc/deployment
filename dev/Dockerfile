ARG BASE_CONTAINER=jupyter/minimal-notebook:5cb007f03275
# History
# 07.12.2020 | 399cbb986c6b
# 29.01.2021 | 5cb007f03275

FROM $BASE_CONTAINER

ARG JUPYTERHUB_VERSION=1.3.0
#RUN python3 -m pip install --upgrade --no-cache-dir jupyterhub==$JUPYTERHUB_VERSION

USER root

# ffmpeg for matplotlib anim & dvipng+cm-super for latex labels
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg dvipng cm-super quantum-espresso && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_UID

RUN conda install --quiet --yes \
    'ipywidgets=7.6.*' \
    'ipympl=0.6.*'\
    'jupyterhub='$JUPYTERHUB_VERSION \
    'matplotlib-base=3.3.*' \
    'gpaw' \
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

ENV GPAW_SETUP_PATH="/home/${NB_USER}/surfer-analysis/jupyter-data/gpaw_potentials"

WORKDIR $HOME

COPY --chown=${NB_UID}:${NB_GID} . agfalta_tools

RUN python3 -m pip install -e agfalta_tools/. && \
    rm -rf agfalta_tools/* && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

