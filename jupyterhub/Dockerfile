FROM jupyterhub/jupyterhub:5.2.1

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install jupyterhub-traefik-proxy==2&& \
    python3 -m pip install dockerspawner==13.0.0 && \
    python3 -m pip install jupyterhub-firstuseauthenticator==1.1.0 && \
    python3 -m pip install jupyterhub-idle-culler==1.4.0 && \
    python3 -m jupyterhub_traefik_proxy.install --traefik --output=/usr/local/bin

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py





