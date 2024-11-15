# Default configuration
REGISTRY    ?= localhost:5000
NAME_BASE   ?= 
VERSION     ?=

# Colors for pretty printing
BLUE        := \033[94m
GREEN       := \033[92m
RED         := \033[91m
RESET       := \033[0m

# List of all targets and their corresponding packages
TARGETS     := uspy gpaw arpes

# Function to get package version from image
define get_version
	VERSION=$$(docker run --rm $(REGISTRY)/$(NAME_BASE)$(1):latest \
		python3 -c "import $(1); print($(1).__version__)" | tail -n 1); \
	if [ -n "$$VERSION" ]; then \
		echo "$(BLUE)Found version $$VERSION for $(1)$(RESET)"; \
	fi
endef

.DEFAULT_GOAL := help

help:
	@echo "$(BLUE)Available targets:$(RESET)"
	@echo "  make build <target>         - Build specific target (base/uspy/gpaw/arpes)"
	@echo "  make push <target>          - Push specific target"
	@echo "  make build-all              - Build all images"
	@echo "  make push-all               - Push all images"
	@echo "  make all                    - Build and push all images"
	@echo "  make version <target>       - Get package version for target"
	@echo "  make clean                  - Remove temporary files"
	@echo "  make prune                  - Clean up docker system"
	@echo ""
	@echo "$(BLUE)Environment variables:$(RESET)"
	@echo "  REGISTRY  - Docker registry (default: $(REGISTRY))"
	@echo "  VERSION   - Version tag (optional, auto-detected if not set)"

# Generic build target
build: TARGET ?= $(word 2,$(MAKECMDGOALS))
build:
	@if [ -z "$(TARGET)" ] || ! echo "$(TARGETS)" | grep -wq "$(TARGET)"; then \
		echo "$(RED)Error: Valid target required. Use one of: $(TARGETS)$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Building $(TARGET) image...$(RESET)"
	@docker build --target $(TARGET) \
		$(if $(and $(filter uspy,$(TARGET)),$(VERSION)),--build-arg USPY_VERSION=$(VERSION),) \
		$(if $(and $(filter gpaw,$(TARGET)),$(VERSION)),--build-arg GPAW_VERSION=$(VERSION),) \
		--tag $(REGISTRY)/$(NAME_BASE)$(TARGET):latest .

	@if [ "$(TARGET)" != "base" ]; then \
		$(call get_version,$(TARGET)); \
		if [ -n "$$VERSION" ]; then \
			docker tag $(REGISTRY)/$(NAME_BASE)$(TARGET):latest $(REGISTRY)/$(NAME_BASE)$(TARGET):$$VERSION; \
		fi \
	fi

# Generic push target
push: TARGET ?= $(word 2,$(MAKECMDGOALS))
push:
	@if [ -z "$(TARGET)" ] || ! echo "$(TARGETS)" | grep -wq "$(TARGET)"; then \
		echo "$(RED)Error: Valid target required. Use one of: $(TARGETS)$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Pushing $(TARGET) image...$(RESET)"
	@docker push $(REGISTRY)/$(NAME_BASE)$(TARGET):latest
	@if [ -z "$(VERSION)" ] && [ "$(TARGET)" != "base" ]; then \
		$(call get_version,$(TARGET)); \
		if [ -n "$$VERSION" ]; then \
			docker push $(REGISTRY)/$(NAME_BASE)$(TARGET):$$VERSION; \
		fi \
	elif [ -n "$(VERSION)" ]; then \
		docker push $(REGISTRY)/$(NAME_BASE)$(TARGET):$(VERSION); \
	fi

# Version detection target
version: TARGET ?= $(word 2,$(MAKECMDGOALS))
version:
	@if [ -z "$(TARGET)" ] || ! echo "$(TARGETS)" | grep -wq "$(TARGET)"; then \
		echo "$(RED)Error: Valid target required. Use one of: $(TARGETS)$(RESET)"; \
		exit 1; \
	fi
	@if [ "$(TARGET)" = "base" ]; then \
		echo "$(BLUE)Base image has no package version$(RESET)"; \
	else \
		$(call get_version,$(TARGET)); \
	fi

# Combined targets
build-all:
	@for target in $(TARGETS); do \
		$(MAKE) build $$target; \
	done
	@echo "$(GREEN)All images built successfully$(RESET)"

push-all:
	@for target in $(TARGETS); do \
		$(MAKE) push $$target; \
	done
	@echo "$(GREEN)All images pushed successfully$(RESET)"

all: build-all push-all

# Utility targets
clean:
	rm -rf version.txt
	@echo "$(GREEN)Cleaned temporary files$(RESET)"

prune:
	@echo "$(BLUE)Cleaning up docker system...$(RESET)"
	docker system prune -f
	@echo "$(GREEN)Docker system cleaned$(RESET)"

# Special target to handle the second argument
%:
	@:

.PHONY: help build push build-all push-all all clean prune version
