# calls the subdirectories' makefiles

update: docker jh-restart

docker:
	$(MAKE) -C docker
	
jh-restart:
	$(MAKE) -C jupyterhub restart

dev-build:
	$(MAKE) -C dev build
	
dev-run:
	$(MAKE) -C dev run


.PHONY: update docker jh-restart dev-build dev-run

