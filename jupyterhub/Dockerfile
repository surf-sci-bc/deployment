# FROM python:3.9.1

# RUN python3 -m pip install jupyterhub && \
#     python3 -m pip install jupyterhub-traefik-proxy && \
#     python3 -m pip install dockerspawner && \
#     python3 -m pip install jupyterhub-firstuseauthenticator && \
#     python3 -m pip install jupyter-client && \
#     python3 -m pip install jupyterhub-idle-culler && \
#     python3 -m pip install pycurl && \
#     python3 -m jupyterhub_traefik_proxy.install --traefik --output=/usr/local/bin

# COPY jupyterhub_config.py /etc/jupyter/jupyterhub_config.py

FROM jupyterhub/jupyterhub:latest

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install jupyterhub && \
    python3 -m pip install jupyterhub-traefik-proxy && \
    python3 -m pip install dockerspawner && \
    python3 -m pip install jupyterhub-firstuseauthenticator && \
    python3 -m pip install jupyter-client && \
    python3 -m pip install jupyterhub-idle-culler && \
    python3 -m pip install pycurl && \
    python3 -m jupyterhub_traefik_proxy.install --traefik --output=/usr/local/bin 
    #python3 -m pip install glob3

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py




