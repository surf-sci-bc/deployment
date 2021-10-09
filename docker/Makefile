NAME		?= localhost:5000/uspy
VERSION     ?=


all: build push

build:
	docker build --build-arg USPY_VERSION=$(VERSION) -t $(NAME):latest .
	@echo "\033[94m### built docker image $(NAME):latest\033[0m"

gettag:
	docker run --rm $(NAME):latest python3 -c "import uspy; print(uspy.__version__)" > version.txt
	docker tag $(NAME):latest $(NAME):$$(cat version.txt)
	@echo "\033[94m### found uspy version $$(cat version.txt)\033[0m"

push: gettag
	docker push $(NAME):$$(cat version.txt)
	docker push $(NAME):latest
	@echo "\033[94m### pushed docker image $(NAME):latest and $(NAME):$$(cat version.txt)\033[0m"

clean:
	rm -rf version.txt

FORCE:

.PHONY: FORCE build push
