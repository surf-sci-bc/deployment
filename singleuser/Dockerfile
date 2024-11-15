ARG BASE_CONTAINER=quay.io/jupyter/scipy-notebook:55942dfe466d
# History
# 07.12.2020 | 399cbb986c6b
# 29.01.2021 | 5cb007f03275
# 27.04.2021 | 584f43f06586
# 07.05.2021 | 09fb66007615
# 06.07.2021 | 7999479a0adc
# 12.08.2021 | 12ba1d59fbc3
# 09.10.2021 | 6f4cbae746cd
# 13.06.2022 | 5cd0b55db86f
# 19.11.2022 | 2ace7f71087a
# 30.01.2023 | 1ffe43816ba9 <-- until here minimal-notebook
# 13.11.2024 | 55942dfe466d <-- From here scipy-notebook images on on quay.io

FROM $BASE_CONTAINER AS base

# Jupyterhub version must match version inside the jupyterhub/Dockerfile
ARG JUPYTERHUB_VERSION=5.2.1

USER root

# ffmpeg for matplotlib anim & dvipng+cm-super for latex labels, gfortran for DFT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends htop && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# The images at jupyter/docker-stacks, where minimal-notebook is pulled from stopped pinning package
# versions. Packages will still be pinned here, to ensure functionality

RUN mamba install --quiet --yes \
    'ipywidgets=8.*' \
    'ipympl=0.9.*'\
    'jupyterlab=4.*' \
    'jupyterhub='$JUPYTERHUB_VERSION \
    'matplotlib-base=3.*' \
    && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME="/home/${NB_USER}/.cache/"

RUN MPLBACKEND=Agg python3 -c "import matplotlib.pyplot" && \
    fix-permissions "/home/${NB_USER}"

#-------------------------
# Make changes below this line to avoid cache busting

WORKDIR $HOME

FROM base AS uspy

# By default, use latest uspy version on PyPI
ARG USPY_VERSION
# Check if uspy_version is set
ARG VERSION=${USPY_VERSION:+:$USPY_VERSION}

# ==== Used only for pypi installation of uspy ====
# Syntax: First line evaluates if $USPY_VERSION is empty.
# If true, && is executed. Else || is.
# The next && lines are executed if either one completes.
#RUN [ -z "${USPY_VERSION}" ] \
#    && pip install uspy \
#    || pip install uspy=="${USPY_VERSION}" \
#    && fix-permissions "${CONDA_DIR}" \
#    && fix-permissions "/home/${NB_USER}"
# ==== END ====


# ==== Used only for local installation of uspy ====
# currently relies on agfalta_tools being in the same directory as the Dockerfile
#COPY --chown=${NB_UID}:${NB_GID} uspy /tmp/uspy

RUN git clone https://github.com/surf-sci-bc/uspy"${VERSION}" /tmp/uspy

RUN python3 -m pip install --no-cache-dir /tmp/uspy/. \
    # Fix for pyclustering not working
    https://github.com/KulikDM/pyclustering/archive/Warning-Fix.zip && \
    rm -rf /tmp/uspy && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
# ==== END ====

FROM base AS gpaw

# By default, use the latest version of gpaw unless GPAW_VERSION is provided
ARG GPAW_VERSION

RUN mamba install --quiet --yes \
    $(if [ -n "$GPAW_VERSION" ]; then echo "gpaw=$GPAW_VERSION"; else echo "gpaw"; fi) \
    && mamba clean --all -f -y \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

# pybind11 is necessary for kplib
RUN python3 -m pip install --no-cache-dir pybind11 && \
    python3 -m pip install --no-cache-dir myqueue spglib kplib && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"


# Fix OpenMPI looking for ssh client, necessary for qe
# Set OpenMPI to use --bind-to core as default for multicore processing

RUN sed -i -e '$aplm_rsh_agent=sh' -e '$ahwloc_base_binding_policy=core' /opt/conda/etc/openmpi-mca-params.conf

FROM base AS arpes

# By default, use the latest version of arpes from GitHub
ARG ARPES_VERSION
RUN git config --global url.https://github.com/.insteadOf git@github.com: && \
    pip install --no-cache-dir "git+https://github.com/arafune/arpes@${ARPES_VERSION:-main}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"


