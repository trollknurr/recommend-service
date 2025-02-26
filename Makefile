#!/usr/bin/make

SHELL = /bin/sh

CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

PROJECT_DIR ?= $(shell pwd)

BUF_IMG ?= bufbuild/buf:1.50.0


format:
	black src/ test/
	ruff check --fix-only --unsafe-fixes src/ test/


lint:
	black --check src/
	ruff check src/
	pyright


#
# Docker
#

rebuild:
	docker compose up --build -d

shell:
	docker compose exec app bash

.PHONY: test
test:
	docker compose exec app pytest test/

down:
	docker compose down --remove-orphans


#
# gRPC
#


.PHONY: local-api-proto-gen
local-api-proto-gen:
	docker run \
		--rm \
    	--volume "${PROJECT_DIR}:/workspace" \
    	--workdir /workspace ${BUF_IMG} \
    	generate /workspace


.PHONY: proto-lint
proto-lint:
	docker run \
		--rm \
    	--volume "${PROJECT_DIR}:/workspace" \
    	--workdir /workspace ${BUF_IMG} \
    	lint /workspace

fixperm:
	sudo chown -R $(CURRENT_UID):$(CURRENT_GID) .
