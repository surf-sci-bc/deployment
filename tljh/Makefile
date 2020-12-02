NAME		:= localhost:5000/agfalta_tools
TAG			 = latest
VERSION := HEAD

all: image

agfalta_tools:
	git clone git@github.com:surf-sci-bc/agfalta_tools.git
	git -C agfalta_tools checkout $(VERSION)

gettag: agfalta_tools FORCE
	$(eval TAG=$$(shell git -C agfalta_tools describe))
	@echo "\033[94m### checked out git $(VERSION)\033[0m"

build: agfalta_tools gettag
	docker build -t $(NAME):$(TAG) -t $(NAME):latest .
	@echo "\033[94m### built docker image $(NAME):$(TAG)\033[0m"

push:
	docker push $(NAME):$(TAG)
	docker push $(NAME):latest
	@echo "\033[94m### pushed docker image $(NAME):$(TAG)\033[0m"

image: build push clean

clean:
	rm -rf agfalta_tools

FORCE:

.PHONY: FORCE image build push clean
