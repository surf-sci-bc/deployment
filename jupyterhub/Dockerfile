FROM jupyterhub/jupyterhub:1.3.0

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install jupyterhub && \
    python3 -m pip install jupyterhub-traefik-proxy && \
    python3 -m pip install dockerspawner && \
    python3 -m pip install jupyterhub-firstuseauthenticator && \
    python3 -m pip install jupyter-client && \
    python3 -m pip install jupyterhub-idle-culler && \
    python3 -m pip install pycurl && \
    python3 -m jupyterhub_traefik_proxy.install --traefik --output=/usr/local/bin 

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py





