# calls the subdirectories' makefiles

update: docker tljh-refresh

docker:
	$(MAKE) -C docker

dev-build:
	$(MAKE) -C dev build
	
dev-run:
	$(MAKE) -C dev run

tljh-config:
	$(MAKE) -C tljh configure

tljh-refresh:
	$(MAKE) -C tljh refresh-config

.PHONY: docker dev-build dev-run tljh-config tljh-refresh
