# Agent Notes — CPU Scheduling Simulator

## Mission
Ship a polished CPU Scheduling Simulator with Gantt charts and comparison views.

## Stack
Python 3.11+, Tkinter, matplotlib, pytest.

## Conventions
- Scheduler return shape: `(list[Process], timeline)` with `(pid|"IDLE", start, end)`.
- Tie-break: lower pid; equal priority → arrival then pid.
- Feature branches per phase; merge to `main`; commit message `Phase X: ...`.

## Status
- Phases 0–12 complete on `main`.
- Public README is product-style (no marks / lab framing).
- Manual follow-ups live in `docs/checklist.md`.

## Run
```bash
python3 -m pip install -r requirements.txt
python3 src/main.py
python3 -m pytest tests/ -v
```
On macOS without Tk in the active interpreter, use Framework Python 3.12+.
