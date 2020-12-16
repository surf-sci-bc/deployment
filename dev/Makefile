IMAGE_NAME  ?= agfalta_tools-dev
CONT_NAME   ?= agfalta_tools_devJL
TAG          = latest
VERSION     ?= HEAD

# If REPO_DIR is given from the command line, the following is ignored (due to "?=").
# If repo_location.txt exists, load the contents as REPO_DIR (can be erased by make clean).
# If it does not exist, fall back to "agfalta_tools" to clone fresh to this directory.
ifneq ($(wildcard ./repo_location.txt),)
	REPO_DIR ?= $(shell cat repo_location.txt)
else
    REPO_DIR ?= agfalta_tools
endif


all: build

# Check if REPO_DIR actually exists and if it is a git repo.
check_repo:
	@if ! [ -d "$(REPO_DIR)" ]; then echo "\033[91mCan't find $(REPO_DIR)\033[0m" && exit 1; fi
	@git -C $(REPO_DIR) describe || { echo "\033[91m$(REPO_DIR) is not a git repository \033[0m"; exit 1; }
	@echo "\033[94m### Using repo location \"$(REPO_DIR)\"\033[0m"

# This is only called if REPO_DIR is agfalta_tools (default)
agfalta_tools:
	git clone git@github.com:surf-sci-bc/agfalta_tools.git
	git -C agfalta_tools checkout $(VERSION)

gettag: FORCE
	$(eval TAG=$$(shell git -C $(REPO_DIR) describe))
	@echo "\033[94m### checked out git $(VERSION)\033[0m"


# This also populates the repo_location.txt file
build: $(REPO_DIR) check_repo gettag
	docker build \
		-t $(IMAGE_NAME):$(TAG) \
		-t $(IMAGE_NAME):latest \
		-f $(CURDIR)/Dockerfile \
		$(REPO_DIR)
	@echo "\033[94m### built docker image \"$(IMAGE_NAME):$(TAG)\"\033[0m"
	@if [ $(REPO_DIR) != agfalta_tools ]; \
		then echo "$(REPO_DIR)" > repo_location.txt; \
	fi

run: check_repo
	docker run \
	    --rm \
		-p 8888:8888 \
		-v $(REPO_DIR):/home/jovyan/agfalta_tools \
		--name $(CONT_NAME) \
		$(IMAGE_NAME):$(TAG)

clean:
	rm -rf agfalta_tools
	rm -f repo_location.txt



FORCE:

.PHONY: FORCE build run clean check_repo gettag

