# Agent Notes — CPU Scheduling Simulator

This file tracks how agents should work in this repo so progress stays consistent across sessions.

## Mission

Build a **CPU Scheduling Simulator with Gantt Charts** as an OS lab mini-project (30 marks), following `plan.md` phase-by-phase.

## Stack Constraints

- Python 3.11+
- Tkinter GUI
- matplotlib for Gantt + comparison charts
- pytest for tests
- No heavy frameworks; Mac-friendly: `pip install matplotlib` (+ pytest from `requirements.txt`)

## Workflow Rules

1. Read `plan.md` before starting work; update the Progress Log when a phase completes.
2. Do **not** skip phases. Complete one phase, commit, summarize, then wait for the user to say **"continue"** unless they asked to run all phases autonomously.
3. Work on **feature branches** named like `phase-0-scaffolding`, `phase-1-models`, etc. Push branches to origin; merge into default branch (`main` once created) when the phase commit is ready.
4. Commit every ~150 lines of new/changed code (running total within a phase), and **always** commit at phase end even if under 150 lines.
5. Commit message format: `Phase X: <short description>`.
6. Before committing, list the files that will be included and show them to the user.
7. Never commit: `__pycache__/`, `.DS_Store`, `*.pyc`, `venv/`, `.pytest_cache/`.
8. Prefer GitHub MCP file push tools when available. If MCP is unavailable (as in some Cursor sessions), fall back to local `git add` / `git commit` / `git push` so commits still appear on `github.com/anubhav-kayal/os-lab-project`.
9. After each commit, report the commit SHA and GitHub URL to the user.
10. Run existing tests before committing once tests exist (`pytest tests/ -v`).

## Return Shape for Schedulers

All scheduling functions should return a consistent structure usable by the GUI:

```python
# Recommended:
# (scheduled_processes: list[Process], timeline: list[tuple[pid|str, start, end]])
# where idle gaps use ("IDLE", start, end)
```

## Tie-Breaking Convention

- Lower `pid` wins ties unless an algorithm specifies otherwise.
- Equal priority falls back to arrival order / FCFS (then pid).

## Current Session Notes

- Default branch on empty remote: create `main` with first push.
- GitHub MCP tools were **not** available in the initial session; ConnectScm + `gh`/`git` used instead.
- Scaffolding stubs already existed locally (empty files) before Phase 0 commit; Phase 0 formalizes and pushes them.

## After Phase 12 Deliverables for User

- Full repo summary
- Total commit count
- Demo-day walkthrough script (process sets, algorithm order, talking points on tie-breaking and idle time)
- Manual checklist (screenshots, report prose, live demo practice)
