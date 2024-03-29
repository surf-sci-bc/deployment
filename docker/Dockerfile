ARG BASE_CONTAINER=jupyter/minimal-notebook:1ffe43816ba9
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
# 30.01.2023 | 1ffe43816ba9

FROM $BASE_CONTAINER

# Jupyterhub version must match version inside the jupyterhub/Dockerfile
ARG JUPYTERHUB_VERSION=3.1.1

# By default, use latest uspy version on PyPI
ARG USPY_VERSION

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
    'gpaw=22.8.*' \
    'ipywidgets=7.6.*' \
    'ipympl=0.9.*'\
    'jupyterhub='$JUPYTERHUB_VERSION \
    'matplotlib-base=3.6.*' \
    'qe=7.*' \
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
COPY --chown=${NB_UID}:${NB_GID} uspy /tmp/uspy

RUN python3 -m pip install --no-cache-dir /tmp/uspy/. && \
    rm -rf /tmp/uspy && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
# ==== END ====
