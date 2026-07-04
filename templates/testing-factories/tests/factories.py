"""factory_boy factories, with example models to demonstrate the patterns.

The ``User``/``Post`` models below are placeholders so the factories have
something to build: sequences for uniqueness, Faker for realistic data,
subfactories for relationships, traits for variants. Replace them with
factories for your own domain models and delete the examples.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

import factory
from factory import Faker, LazyFunction, Sequence, SubFactory, Trait


@dataclass
class User:
    id: int
    username: str
    email: str
    role: str = "user"
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Post:
    id: int
    title: str
    author: User
    published_at: datetime | None = None

    @property
    def is_published(self) -> bool:
        return self.published_at is not None


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = Sequence(lambda n: n)
    username = Sequence(lambda n: f"user{n}")
    email = Faker("email")


class AdminUserFactory(UserFactory):
    username = Sequence(lambda n: f"admin{n}")
    role = "admin"


class PostFactory(factory.Factory):
    class Meta:
        model = Post

    class Params:
        published = Trait(published_at=LazyFunction(lambda: datetime.now(UTC)))

    id = Sequence(lambda n: n)
    title = Faker("sentence", nb_words=4)
    author = SubFactory(UserFactory)
