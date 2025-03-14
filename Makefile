#!/usr/bin/make

SHELL = /bin/sh

CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

PROJECT_DIR ?= $(shell pwd)

BUF_IMG ?= bufbuild/buf:1.50.0

IMAGE_NAME ?= recommend-service

format:
	black src/ test/
	ruff check --fix-only --unsafe-fixes src/ test/


lint:
	black --check src/
	ruff check src/
	pyright


lintC:
	docker run --rm $(IMAGE_NAME) black --check src/
	docker run --rm $(IMAGE_NAME) ruff check src/
	docker run --rm $(IMAGE_NAME) pyright

testC:
	docker run --rm $(IMAGE_NAME) pytest test/ -vv

#
# Docker
#

rebuild:
	docker compose up --build -d

shell:
	docker compose exec app bash

logs:
	docker compose logs -f --tail 100

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


#
# ONNX
#
model-convert: export PYTHONPATH=src:src/grpc_proto
model-convert:
	python -m entrypoint.model_convert


#
# Test client
#

test-client: export PYTHONPATH=src:src/grpc_proto
test-client:
	python -m entrypoint.test_client


#
# Utils
# 
fixperm:
	sudo chown -R $(CURRENT_UID):$(CURRENT_GID) .
