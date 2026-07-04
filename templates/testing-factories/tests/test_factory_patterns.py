"""Demonstrates the factory patterns. Replace alongside tests/factories.py."""

from __future__ import annotations

from tests.factories import AdminUserFactory, PostFactory, UserFactory


def test_sequences_generate_unique_values():
    assert UserFactory().username != UserFactory().username


def test_overrides_beat_defaults():
    user = UserFactory(email="fixed@example.com")
    assert user.email == "fixed@example.com"


def test_subclass_factories_specialise():
    assert AdminUserFactory().role == "admin"


def test_subfactories_build_related_objects():
    post = PostFactory()
    assert post.author.is_active


def test_traits_toggle_variants():
    assert PostFactory(published=True).is_published
    assert not PostFactory().is_published


def test_batches_build_many_unique_objects():
    users = UserFactory.build_batch(3)
    assert len({u.username for u in users}) == 3


def test_fixtures_from_conftest(published_post):
    assert published_post.is_published
    assert published_post.author.is_active
