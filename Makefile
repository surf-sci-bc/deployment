# calls the subdirectories' makefiles

update: docker tljh-refresh

docker:
	$(MAKE) -C docker

tljh-config:
	$(MAKE) -C tljh configure

tljh-refresh:
	$(MAKE) -C tljh refresh-config

.PHONY: docker
