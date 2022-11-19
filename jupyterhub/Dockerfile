FROM jupyterhub/jupyterhub:3.0.0

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install jupyterhub-traefik-proxy==0.3.0 && \
    python3 -m pip install dockerspawner==12.1.0 && \
    python3 -m pip install jupyterhub-firstuseauthenticator==1.0.0 && \
    python3 -m pip install jupyterhub-idle-culler==1.2.1 && \
    python3 -m jupyterhub_traefik_proxy.install --traefik --output=/usr/local/bin

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py





