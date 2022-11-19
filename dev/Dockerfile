ARG BASE_CONTAINER=jupyter/minimal-notebook:5cd0b55db86f
# History
# 07.12.2020 | 399cbb986c6b
# 29.01.2021 | 5cb007f03275
# 27.04.2021 | 584f43f06586
# 07.05.2021 | 09fb66007615
# 06.07.2021 | 7999479a0adc
# 12.08.2021 | 12ba1d59fbc3
# 09.10.2021 | 6f4cbae746cd
# 15.05.2022 | 5cd0b55db86f
# 19.11.2022 | 5a26d88e1949

FROM $BASE_CONTAINER

# Jupyterhub version must match version inside the jupyterhub/Dockerfile
ARG JUPYTERHUB_VERSION=3.0.0

USER root

# ffmpeg for matplotlib anim & dvipng+cm-super for latex labels
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg dvipng cm-super libhdf5-serial-dev netcdf-bin libnetcdf-dev build-essential wkhtmltopdf&& \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# The images at jupyter/docker-stacks, where minimal-notebook is pulled from stopped pinning package
# versions. Packages will still be pinned here to ensure functionality

RUN conda install --quiet --yes \
    'ipywidgets=7.6.*' \
    'ipympl=0.9.*'\
    'jupyterhub='$JUPYTERHUB_VERSION \
    'matplotlib-base=3.5.*' \
    #'gcc' \
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

# currently relies on uspy being in the same directory as the Dockerfile
COPY --chown=${NB_UID}:${NB_GID} . uspy

RUN python3 -m pip install -e uspy/. && \
    rm -rf uspy/* && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
