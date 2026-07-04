"""Property-based tests with Hypothesis. Replace the demonstration properties.

Hypothesis generates many inputs per test and shrinks any failure to a
minimal example. Failing examples are stored in ``.hypothesis/`` and replayed
first on the next run, so a red test stays red until actually fixed. Write
properties against your own domain logic (invariants, round-trips,
idempotence) and delete these demonstrations.
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st


@given(st.lists(st.integers()))
def test_sorting_is_idempotent(xs):
    once = sorted(xs)
    assert sorted(once) == once


@given(st.text())
def test_utf8_encoding_round_trips(s):
    assert s.encode("utf-8").decode("utf-8") == s


@given(st.text(min_size=1), st.text(min_size=1))
@settings(max_examples=200)
def test_concatenation_preserves_length(a, b):
    assert len(a + b) == len(a) + len(b)
