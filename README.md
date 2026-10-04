# python-templates

[Copier](https://copier.readthedocs.io/) templates for Python projects built
for agent-driven development: a **base** project with a deterministic quality
gauntlet, plus **mix-ins** you layer on when you need them. Not monolithic by
design — a new project starts small, and structure arrives as it grows.

## Why the gauntlet

An agent will sometimes hallucinate an API, skip a test, lower the bar, or
declare work finished when it isn't. Reviewing harder doesn't scale;
deterministic checks do. The base template wires one command,
`uv run poe check` (lint → format → types → imports → complexity → tests),
into three enforcement points: the agent's contract (AGENTS.md), a pre-commit
hook, and CI. Every gate passes or fails deterministically, with output an
agent can read and act on.

## Start a new project

```
uvx copier copy gh:MarkGravestock/python-templates my-project
cd my-project
git init
uv run poe setup && uv run poe check && uv run poe hooks
```

Copier asks for the project and package name and fills them in everywhere —
no find-and-replace.

## Apply a mix-in later

From inside an existing project generated from base:

```
uvx copier copy --data template=testing-factories gh:MarkGravestock/python-templates .
uv add --dev factory-boy faker
uv run poe check
```

Copier prints each mix-in's remaining steps (the `uv add`, any config) after
copying.

## Templates

| Template             | What it gives you                                                        |
| -------------------- | ------------------------------------------------------------------------ |
| `base`               | src layout with a ports-and-adapters sample, the full poe gauntlet (ruff + bandit rules, pyright, import-linter, radon complexity ceiling, pytest + coverage floor), pip-audit task, AGENTS.md/CLAUDE.md/TABNINE.md contract, `cosmic-python` architecture skill, cross-platform pre-commit hook, GitHub Actions CI (Ubuntu + Windows), renovate.json |
| `testing-factories`  | factory_boy + faker test structure: `tests/factories.py` (sequences, Faker, subfactories, traits), shared conftest fixtures, and pattern-demonstrating tests |
| `testing-property`   | Hypothesis property-based testing: demonstration properties (invariants, round-trips, idempotence) that run inside the existing test gate |
| `testing-mutation`   | mutmut mutation testing as a weekly/manual GitHub Actions job — audits whether the tests would catch bugs, the complement to the coverage floor |
| `testing-containers` | testcontainers integration test against a real Redis in Docker, marked `integration` and self-skipping where Docker is absent |

More candidates (HTTP stubbing, contract testing, BDD, performance) are
parked in [TODO.md](TODO.md).

## How the templates stay proven

CI in this repo generates a project from `base`, runs the full gauntlet on
the output on Ubuntu and Windows, then overlays every mix-in and runs it
again. A template change that would break a generated project cannot merge.

## Adding a mix-in

Create `templates/<name>/` containing only the files the mix-in adds (never
files base already owns — Copier overlays, it does not merge), add the name
to the `template` choices in `copier.yml`, document any `uv add` step in
`_message_after_copy`, and add it to the CI overlay job.
