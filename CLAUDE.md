# AI News & Vocabulary Agent

Daily pipeline: collect English AI news -> translate to JP/VI -> extract technical terms -> count occurrences (SQLite) -> 3 PDFs (EN/JP/VI) -> Anki flashcards.
Full spec: `docs/SPEC.md`. Current state: `PROGRESS.md`. Read both before starting any task.

## Stack
- Python, SQLite (stdlib `sqlite3`), pytest
- ReportLab for PDF (Phase 3), LLM API for translation and term selection ONLY
- APScheduler or cron (Phase 5), Anki + AnkiConnect (Phase 4, not locked)
- Dev machine: Windows + PowerShell. Use `pathlib`; always set `encoding="utf-8"` (JP/VI text).

## Locked decisions (do not change without asking)
- Counting is occurrence-based, on the original English article only, done in Python, never by the LLM.
- Color is per occurrence, in reading order, from the cumulative count: 1 = red, 2-5 = yellow, 6+ = green.
- SQLite is the single source of truth. Never rely on chat or LLM memory.
- LLM returns a term list only; Python finds term positions in the text.
- Re-running an already processed article must NOT change counts or create duplicate cards.
- Merge only clear variants (case, singular/plural). Never auto-merge related terms.
- One flashcard per concept, created when the concept is first seen.
- Default ~3 articles/day, configurable. PDFs are for personal study, not public sharing.
- Nothing from SPEC section 11 (post-MVP) unless asked.

## Working rules
- One task at a time, taken from `PROGRESS.md`.
- Before coding: state the plan in plain language and wait for approval.
- If context is unclear, stop and ask. Never guess.
- Before any non-trivial decision: research, compare trade-offs against the current state, state the problem in plain language, then recommend.
- Write tests first for DB and counting logic.
- YAGNI, KISS, DRY. No extra features, abstractions or dependencies "for later".
- The user is a student who must explain every line in interviews: keep code simple, and explain each change in plain language with a short real-life analogy.
- Do not commit or push. Propose a commit message at the end of each task.

## Definition of done (per task)
1. Tests pass (`python -m pytest`).
2. The user confirms they can explain the new code.
3. `PROGRESS.md` updated (task checked, log entry added).
4. No unrelated changes in the diff.
