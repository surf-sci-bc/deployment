
all: configure test

configure:
	sudo cp jupyterhub_config.py /opt/tljh/config/jupyterhub_config.d
	sudo tljh-config reload

test:
	@echo "I AM A TEST"
