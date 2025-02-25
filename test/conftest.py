import pytest

from entrypoint.config import Config


@pytest.fixture()
def config():
    return Config()
