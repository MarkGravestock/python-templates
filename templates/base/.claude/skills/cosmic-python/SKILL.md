---
name: cosmic-python
description: Structure or review Python code using the Cosmic Python (Architecture Patterns with Python) approach - domain model, repository, service layer, unit of work, domain events and message bus. Use when designing a new Python service or module, deciding where logic belongs, or reviewing layering and test strategy.
---

# Cosmic Python layout

Reference: <https://www.cosmicpython.com/book/preface.html>. Defer to the book for
detail; this skill only fixes the conventions to apply here.

## Layers and dependency direction

Dependencies point inwards only: `entrypoints -> service_layer -> domain`, and
`adapters -> domain`. The domain imports nothing from the other layers or from
frameworks/ORMs.

```
src/<pkg>/
  domain/         # entities, value objects, aggregates, events, commands (plain Python)
  service_layer/  # handlers, unit of work abstraction, message bus
  adapters/       # repository + UoW implementations, ORM mapping, external clients
  entrypoints/    # HTTP/CLI/queue consumers - thin, translate to commands
  bootstrap.py    # composition root: wires adapters into handlers
tests/{unit,integration,e2e}/
```

This project starts with only `domain/` and `cli/` (an entrypoint). Add the other
layers when the code needs them, and add each new package to the layers contract
in `importlinter.ini` so `uv run poe imports` enforces the direction above.

## Rules

- **Domain model**: behaviour lives on entities/aggregates; value objects are
  immutable (frozen dataclasses). No I/O, no ORM base classes.
- **Aggregate = consistency boundary**: one repository per aggregate; other
  aggregates are referenced by id; one aggregate changed per transaction.
- **Repository**: abstract port (`add`, `get`) in the service layer or domain;
  implementations in `adapters/`. Provide an in-memory fake for tests.
- **Unit of Work**: abstract context manager owning the transaction and exposing
  repositories; handlers call `uow.commit()` explicitly.
- **Service layer**: one handler per command, orchestrating load, domain call,
  commit. Handlers take primitives or command objects, never web/ORM types.
- **Events**: aggregates record domain events; the message bus dispatches them
  after commit. Cross-aggregate/side-effect work belongs in event handlers.
- **Entrypoints**: no business logic; build a command, call the bus.
- **Dependency injection**: wire in `bootstrap.py`, not via globals or imports
  of concrete adapters in handlers.
- **Don't over-apply**: for simple CRUD, skip layers rather than adding ceremony.
  Say so when deviating.

## Testing

- Most tests are fast unit tests through the service layer using fake
  repository/UoW; a few integration tests per adapter; a handful of e2e tests.
- Domain model gets focused unit tests with no fakes at all.
- Prefer testing behaviour via commands/handlers over testing internals.
