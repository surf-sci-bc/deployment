# calls the subdirectories' makefiles

docker:
	$(MAKE) -C docker

tljh-config:
	$(MAKE) -C tljh configure

.PHONY: docker
