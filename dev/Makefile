NAME		:= agfalta_tools
TAG			 = latest
VERSION := HEAD
REPO_DIR := /path/to/projects/agfalta_tools

all: build

agfalta_tools:
	git clone git@github.com:surf-sci-bc/agfalta_tools.git
	git -C agfalta_tools checkout $(VERSION)

gettag: agfalta_tools FORCE
	$(eval TAG=$$(shell git -C agfalta_tools describe))
	@echo "\033[94m### checked out git $(VERSION)\033[0m"

build: agfalta_tools gettag
	docker build \
				-t $(NAME):$(TAG)-dev \
				-t $(NAME):latest-dev \
				-f $(CURDIR)/Dockerfile \
				$(REPO_DIR)
	@echo "\033[94m### built docker image $(NAME):$(TAG)\033[0m"

run:
	docker run \
				 -p 8888:8888 \
				 -v $(REPO_DIR):/home/jovyan/agfalta_tools \
				 localhost:5000/agfalta_tools:latest-dev
				 #-e NB_UID=$(id -u)  \
clean:
	rm -rf agfalta_tools

FORCE:

.PHONY: FORCE build push clean
