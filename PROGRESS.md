# Progress

## Current
Phase 1, Task 1.2 (not started)

## Phase 1: Vocabulary Memory Engine
Goal: counting engine that is correct, persistent and safe to re-run. No LLM, no PDF yet.

- [x] 1.0 Repo setup: venv, folder structure, `.gitignore`, pytest runs an empty test
- [x] 1.1 SQLite schema: `concept`, `occurrence`, `article` (fields per SPEC section 4)
- [ ] 1.2 Term normalization: case and singular/plural variants only
- [ ] 1.3 Color rule: pure function, occurrence number -> red / yellow / green
- [ ] 1.4 Record an article's occurrences: update counts, assign each occurrence its color in reading order (e.g. count 4 + 3 new -> yellow, green, green)
- [ ] 1.5 Idempotency: re-running the same article changes nothing
- [ ] 1.6 Persistence: data survives restart
- [ ] 1.7 Phase 1 review: README section, cleanup, confirm SPEC section 10 items for the engine

## Later phases (detail only when reached)
- Phase 2: news collection and term extraction (test EN->JP mapping early, before PDF work)
- Phase 3: translation and 3 PDFs
- Phase 4: flashcards
- Phase 5: daily automation

## Log (newest first)
- 2026-11-26: 1.1 done. Added `src/vocab/db.py` (`connect` turns on foreign keys, `create_schema` creates `article`, `concept`, `occurrence`) and `tests/test_db.py` (7 tests: columns, schema re-run, default count 0, unique canonical_term, unique url, unique (article_id, start_pos), foreign key). `python -m pytest`: 8 passed. Decisions: article identity = URL (content hash left for Phase 2); `occurrence_count` stored as a column per SPEC 4, to be kept in sync with `occurrence` rows in one transaction in 1.4; occurrence stores `occurrence_number`, color is derived (1.3); both `canonical_term` (match key) and `english_term` (display) kept.
- 2026-11-24: 1.0 done. Python 3.14.10 venv in `.venv`, pytest 9.2.0 pinned in `requirements.txt`, pytest config in `pyproject.toml` (`src` on path, tests in `tests`), empty `vocab` package, smoke test passes. Spec renamed to `docs/SPEC.md`.

## Handoff prompt for a new chat
Read CLAUDE.md, PROGRESS.md and docs/SPEC.md. Summarize the current task and the plan in plain language, then wait for my approval before writing code.
