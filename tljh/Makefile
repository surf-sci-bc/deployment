
all: configure

configure:
	sudo cp jupyterhub_config.py /opt/tljh/config/jupyterhub_config.d
	sudo tljh-config reload

refresh-config:
	sudo tljh-config reload
