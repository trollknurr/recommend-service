#!/usr/bin/make

SHELL = /bin/sh

CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

PROJECT_DIR ?= $(shell pwd)


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

test-unit:
	docker compose exec app pytest test/unit

down:
	docker compose down --remove-orphans

migrate:
	docker compose exec app alembic upgrade head

ui:
	docker compose exec app python -m command.ui

report_stuck:
	docker compose exec app python -m command.stuck_jobs_reporter

#
# gRPC
#

.PHONY: vsa-client-gen
vsa-client-gen:
	docker run --volume "${PROJECT_DIR}:/workspace" \
		 --volume "${SSH_DIR}:/root/.ssh" \
		--workdir /workspace ${BUF_IMG} \
		generate --template=buf.gen.yaml ${VSA_REPO_URL}#tag=${VSA_REPO_TAG}

.PHONY: vtt-client-gen
vtt-client-gen:
	docker run --volume "${PROJECT_DIR}:/workspace" \
		 --volume "${SSH_DIR}:/root/.ssh" \
		--workdir /workspace ${BUF_IMG} \
		generate --template=buf.gen.yaml ${VTT_REPO_URL}#tag=${VTT_REPO_TAG}

.PHONY: pub-deliverer-client-gen
pub-deliverer-client-gen:
	docker run --volume "${PROJECT_DIR}:/workspace" \
		 --volume "${SSH_DIR}:/root/.ssh" \
		--workdir /workspace ${BUF_IMG} \
		generate --template=buf.gen.yaml ${PUB_DELIVERER_REPO_URL}#tag=${PUB_DELIVERER_REPO_TAG}

.PHONY: text-4-video-client-gen
text-4-video-client-gen:
	docker run --volume "${PROJECT_DIR}:/workspace" \
		 --volume "${SSH_DIR}:/root/.ssh" \
		--workdir /workspace ${BUF_IMG} \
		generate --template=buf.gen.yaml ${TEXT_4_VIDEO_REPO_URL}#tag=${TEXT_4_VIDEO_REPO_TAG}


.PHONY: video-factory-client-gen
video-factory-client-gen:
	docker run --volume "${PROJECT_DIR}:/workspace" \
		 --volume "${SSH_DIR}:/root/.ssh" \
		--workdir /workspace ${BUF_IMG} \
		generate --template=buf.gen.yaml ${VIDEO_FACTORY_REPO_URL}#tag=${VIDEO_FACTORY_REPO_TAG}


.PHONY: auto-video-editor-client-gen
auto-video-editor-client-gen:
	docker run --volume "${PROJECT_DIR}:/workspace" \
		 --volume "${SSH_DIR}:/root/.ssh" \
		--workdir /workspace ${BUF_IMG} \
		generate --template=buf.gen.yaml ${AUTO_VIDEO_EDITOR_URL}#tag=${AUTO_VIDEO_EDITOR_TAG}


.PHONY: local-api-proto-gen
local-api-proto-gen:
	docker run \
		--rm --platform linux/amd64 \
    	--volume "${PROJECT_DIR}:/workspace" \
    	--workdir /workspace ${BUF_IMG} \
    	generate /workspace

.PHONY: all-proto-gen
all-proto-gen: vsa-client-gen vtt-client-gen pub-deliverer-client-gen text-4-video-client-gen video-factory-client-gen local-api-proto-gen

fixperm:
	sudo chown -R $(CURRENT_UID):$(CURRENT_GID) .

install: export POETRY_HTTP_BASIC_GITLAB_USERNAME=${GITLAB_PYPI_USERNAME}
install: export POETRY_HTTP_BASIC_GITLAB_PASSWORD=${GITLAB_PYPI_PASSWORD}
install:
	poetry install --no-root --with dev