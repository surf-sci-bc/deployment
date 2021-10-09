all: build

restart:
	docker-compose restart

rebuild:
	docker build -t agfalta/jupyterhub .
	docker-compose down
	docker-compose up -d

clean:
	rm -rf uspy
	rm -f repo_location.txt



FORCE:

.PHONY: FORCE build run clean check_repo gettag

