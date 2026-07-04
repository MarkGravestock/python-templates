"""Shared fixtures built on the factories in tests/factories.py."""

from __future__ import annotations

import pytest
from tests.factories import Post, PostFactory, User, UserFactory


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def users() -> list[User]:
    return UserFactory.build_batch(5)


@pytest.fixture
def published_post(user: User) -> Post:
    return PostFactory(author=user, published=True)
