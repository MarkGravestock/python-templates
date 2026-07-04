# TODO: candidate mix-ins

Testing mix-ins considered and deferred (2026-07-04). Each should follow the
existing rules: only files no other template owns, register in `copier.yml`,
document `uv add` steps in `_message_after_copy`, and join the CI overlay job.

- **testing-http** — stubbing outbound HTTP at unit level: `respx` (for
  httpx) or `responses` (for requests), plus `pytest-httpserver` when a real
  listening socket is needed. WireMock via testcontainers is an option for
  stubbing parity with JVM projects.
- **testing-contract** — `schemathesis` first (property-tests an API against
  its OpenAPI spec; a self-contained CI gate). `pact-python` only when there
  are genuine consumer-driven contracts between separately-deployed services
  and a broker to share them. Both presuppose an API, so this layers on an
  `api` mix-in that does not exist yet.
- **testing-bdd** — `pytest-bdd` (stays inside the pytest gate). Only worth
  the Gherkin ceremony when non-developers read the feature files; otherwise
  prefer test DSLs/builders on top of testing-factories.
- **testing-perf** — `pytest-benchmark` for micro-benchmarks, advisory/on
  demand rather than a CI gate (shared-runner noise makes regression gates
  flaky). `locust` for load-testing a running service is an operational tool,
  not a gauntlet gate.
- **api** — prerequisite for testing-contract and "test your own API" HTTP
  testing: FastAPI (or similar) adapter layer + httpx `TestClient`, wired
  into the import-linter layers contract.
