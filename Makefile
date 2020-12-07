# calls the subdirectories' makefiles

update: docker tljh-refresh

docker:
	$(MAKE) -C docker

dev:
	$(MAKE) -C dev

tljh-config:
	$(MAKE) -C tljh configure

tljh-refresh:
	$(MAKE) -C tljh refresh-config

.PHONY: docker
