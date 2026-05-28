# FennFlow — Development Context

## Target Audience

Python developers who need structured, transactional-like file
operations on S3-compatible storage, particularly in:

- Web backends (FastAPI, Django async, etc.)
- Data pipelines requiring atomic multi-file operations
- Any domain needing SSOT + Saga guarantees over object storage

## Key Design Pillars

1. SSOT — backend is source of truth, not the file storage
2. Saga compensation — automatic rollback on failure
3. Clean Architecture — repository mixins (Put/Get/Delete/List/Create)
4. Pydantic-powered content models
5. Testability — InMemory swap, zero mocks

## Architecture Reference

See llms-full.txt for full architecture documentation.

## Versioning Policy

- Current: 0.4.0 (Alpha)
- Next milestone: beta (closes when record locks #55 ships)
- After ~6 months real-world usage: 1.0.0 / Production Stable
- Semver strictly followed from 1.0.0 onward

## Test Coverage: ~90%

## Intentional Design Decisions

- No garbage collection (separate worker planned, issue #48)
- No distributed locking until record locks (#55) ships
- Backend is mandatory (no NoOpBackend — rejected, issue #15)
- SQLAlchemy is default backend (not Redis, not raw memory)

## Inspiration / Comparisons

- SQLAlchemy Unit of Work pattern
- Saga pattern (microservices compensation)
- NOT an Outbox pattern implementation (by design — no relay process)