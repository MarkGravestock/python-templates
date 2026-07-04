"""Integration test demonstrating testcontainers: a real Redis in Docker.

Marked ``integration`` (declared in pyproject.toml) and skipped wherever
Docker is unavailable, so the gauntlet stays green on machines without it.
Replace with containers for the services your project actually uses
(PostgreSQL, Kafka, ...) — see https://testcontainers-python.readthedocs.io/.
"""

from __future__ import annotations

import pytest
from testcontainers.redis import RedisContainer


def _docker_available() -> bool:
    try:
        from testcontainers.core.docker_client import DockerClient

        DockerClient().client.ping()
    except Exception:  # docker missing, not running, or misconfigured
        return False
    return True


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _docker_available(), reason="Docker is not available"),
]


def test_redis_round_trip():
    with RedisContainer() as container:
        client = container.get_client()
        client.set("greeting", "hello")
        assert client.get("greeting") == b"hello"
