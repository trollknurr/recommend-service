import logging
from loguru import logger

from typing import Generator

import pytest
from dependency_injector import providers

from entrypoint.config import Config
from entrypoint.grpc_server.container import Container


@pytest.fixture(scope="session")
def test_config():
    return Config(ENV="test")


@pytest.fixture(scope="session")
def test_container(test_config: Config) -> Generator[Container, None, None]:
    container = Container(config_obj=providers.Object(test_config))
    container.init_resources()

    yield container

    container.shutdown_resources()
