ARG BASE_CONTAINER=jupyter/minimal-notebook:12ba1d59fbc3
# History
# 07.12.2020 | 399cbb986c6b
# 29.01.2021 | 5cb007f03275
# 27.04.2021 | 584f43f06586
# 07.05.2021 | 09fb66007615
# 06.07.2021 | 7999479a0adc
# 12.08.2021 | 12ba1d59fbc3

FROM $BASE_CONTAINER

# Jupyterhub version must match version inside the jupyterhub/Dockerfile
ARG JUPYTERHUB_VERSION=1.4.2

USER root

# ffmpeg for matplotlib anim & dvipng+cm-super for latex labels, gfortran for DFT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg dvipng cm-super gfortran texlive-science cmake htop && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install AQuaLEED

WORKDIR /usr/local/src

RUN wget https://physics.mff.cuni.cz/kfpp/povrchy/files/1243-AQuaLEED-2.0.3a.tar.bz2 --progress=dot:giga -O AQuaLEED.tar.bz2 && \
    mkdir AQuaLEED && \
    tar -xvf AQuaLEED.tar.bz2 -C AQuaLEED && \
    rm AQuaLEED.tar.bz2 && \
    mv AQuaLEED/compilers-linux.ini AQuaLEED/compilers.ini && \
    sed -i 's|\\data|/data|' AQuaLEED/defaults.ini && \
    sed -i 's|FTN95-CHECKMATE|gfortran|' AQuaLEED/defaults.ini && \
    mv AQuaLEED/AQuaLEED.sh /usr/local/bin/aqualeed && \
    sed -i -e '$apython3 /usr/local/src/AQuaLEED/aqualeed.py "$@"' -e '$d' /usr/local/bin/aqualeed

# Apply Bugfix
RUN wget https://physics.mff.cuni.cz/kfpp/povrchy/files/1407-satleed-common.f --progress=dot:giga -O /usr/local/src/AQuaLEED/LEED-codes/satleed_common.f

USER $NB_UID

# The images at jupyter/docker-stacks, where minimal-notebook is pulled from stopped pinning package
# versions. Packages will still be pinned here, to ensure functionality 

RUN conda install --quiet --yes \
    'atomsk=0.11.*' \
    'gpaw=21.6.*' \
    'ipywidgets=7.6.*' \
    'ipympl=0.7.*'\
    'jupyterhub='$JUPYTERHUB_VERSION \
    'matplotlib-base=3.4.*' \
    'qe=6.7.*' \
    && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Fix OpenMPI looking for ssh client, necessary for qe
# Set OpenMPI to use --bind-to core as default for multicore processing

RUN sed -i -e '$aplm_rsh_agent=sh' -e '$ahwloc_base_binding_policy=core' /opt/conda/etc/openmpi-mca-params.conf

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME="/home/${NB_USER}/.cache/"

RUN MPLBACKEND=Agg python3 -c "import matplotlib.pyplot" && \
    fix-permissions "/home/${NB_USER}"

#-------------------------
# Make changes below this line to avoid cache busting

WORKDIR $HOME

# currently relies on agfalta_tools being in the same directory as the Dockerfile
COPY --chown=${NB_UID}:${NB_GID} agfalta_tools /tmp/agfalta_tools

RUN python3 -m pip install --no-cache-dir /tmp/agfalta_tools/. && \
    rm -rf /tmp/agfalta_tools && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
