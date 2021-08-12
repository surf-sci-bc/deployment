FROM jupyterhub/jupyterhub:1.4.2

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install jupyterhub-traefik-proxy==0.2.0 && \
    python3 -m pip install dockerspawner==12.1.0 && \
    python3 -m pip install jupyterhub-firstuseauthenticator==0.14.1 && \
    python3 -m pip install jupyterhub-idle-culler==1.1 && \
    python3 -m jupyterhub_traefik_proxy.install --traefik --output=/usr/local/bin 

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py





