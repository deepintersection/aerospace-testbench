# Contributing to aerospace-testbench

## Quick start

### Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | ≥ 3.11 | Via `pyenv` or system |
| [uv](https://docs.astral.sh/uv/) | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Docker + Compose | latest | For PostgreSQL in dev |
| NI-VISA **or** linux-gpib | — | HOST only, for real instrument I/O |

### Set up the dev environment

```bash
git clone https://github.com/deepintersection/aerospace-testbench
cd aerospace-testbench

# Install all dependencies (including dev extras) into an isolated venv
uv sync --extra dev

# Copy environment template and edit
cp .env.example .env

# Start PostgreSQL
docker compose up -d postgres

# Apply migrations (once the migrations/ directory exists, PR 3+)
uv run alembic upgrade head

# Run the API (host, not Docker — needed for instrument access)
uv run uvicorn aerospace_testbench.api.main:app --reload
```

### Run tests

```bash
# All unit tests (no hardware, no DB required)
uv run pytest -m "not integration and not hardware"

# Unit + integration tests (PostgreSQL must be running)
uv run pytest -m "not hardware"

# Full suite on a lab machine with instruments connected
uv run pytest
```

---

## Branch & PR workflow

This project develops in **tiny, reviewable steps**.  Every change lands via a
pull request — even one-line fixes.

### Branch naming

```text
feat/<short-description>      # new feature / domain object
fix/<short-description>       # bug fix
chore/<short-description>     # tooling, deps, config
docs/<short-description>      # documentation only
```

### PR rules

1. **One bounded context per PR** — a PR that touches `project_registry` and
   `campaign` simultaneously will be asked to split.
2. **Tests included** — every new public function ships with at least one test
   in the same PR.
3. **No broken CI** — the branch must pass lint, type-check, and unit tests
   before review.
4. **PR description must state**: what changed, why, and which roadmap step
   it corresponds to.

### CodeRabbit

CodeRabbit reviews every PR automatically.  Address all "Request changes"
comments before requesting human review.  "Nitpick" comments are optional but
encouraged to discuss.

---

## Architecture rules (DDD)

```text
src/aerospace_testbench/
├── project_registry/     # Bounded context — no imports from other BCs
├── dut/                  # Bounded context
├── instrument_control/   # Bounded context — infrastructure layer
├── campaign/             # Bounded context
├── monitoring/           # Bounded context
├── reporting/            # Bounded context
└── api/                  # FastAPI app — thin adapter, no domain logic
```

- **Domain models** live in `domain.py` inside each BC.  No framework imports.
- **Repositories** in `repository.py` — only place that touches SQLAlchemy.
- **Services** in `service.py` — orchestrate domain objects, call repositories.
- **Schemas** in `schemas.py` — Pydantic models for API I/O only.

---

## Instrument safety

> ⚠️  These rules protect both the hardware under test and the test equipment.

- **Never** send a command to a real instrument without checking the
  `INSTRUMENT_BACKEND` environment variable first.
- Hardware tests are marked `@pytest.mark.hardware` and **never run in CI**.
- All VISA `write()` calls must include an explicit timeout.
- Log the instrument VISA address and command in every error handler.
- If you are unsure whether a command is safe to send to a powered DUT,
  **do not merge** — raise it in the PR discussion.

---

## Code style

- Formatter: `ruff format` (line length 100)
- Linter: `ruff check`
- Type checker: `mypy --strict`

Run all checks before pushing:

```bash
uv run ruff format .
uv run ruff check .
uv run mypy src/
```
