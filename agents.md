# Agent Notes — CPU Scheduling Simulator

This file tracks how agents should work in this repo so progress stays consistent across sessions.

## Mission

Build a **CPU Scheduling Simulator with Gantt Charts** as an OS lab mini-project (30 marks), following `plan.md` phase-by-phase.

## Stack Constraints

- Python 3.11+
- Tkinter GUI
- matplotlib for Gantt + comparison charts
- pytest for tests
- No heavy frameworks; Mac-friendly: `pip install -r requirements.txt`

## Workflow Rules

1. Read `plan.md` before starting work; update the Progress Log when a phase completes.
2. Do **not** skip phases. Complete one phase, commit, summarize; wait for **"continue"** unless the user asked to run multiple phases autonomously.
3. Work on **feature branches** named like `phase-1-models`, `phase-2-fcfs`, etc. Push branches; update `main` after each phase commit.
4. Commit every ~150 lines of new/changed code within a phase, and **always** commit at phase end.
5. Commit message format: `Phase X: <short description>`.
6. Before committing, list the files included.
7. Never commit: `__pycache__/`, `.DS_Store`, `*.pyc`, `venv/`, `.pytest_cache/`.
8. Prefer GitHub MCP when available; otherwise `git` + `git push` to `github.com/anubhav-kayal/os-lab-project`.
9. After each commit, report the commit SHA and GitHub URL.
10. Run existing tests before committing once tests exist (`pytest tests/ -v`).

## Return Shape for Schedulers

```python
# (scheduled_processes: list[Process], timeline: list[tuple[pid|str, start, end]])
# Idle gaps use ("IDLE", start, end)
```

## Tie-Breaking Convention

- Lower `pid` wins ties unless an algorithm specifies otherwise.
- Equal priority falls back to arrival order / FCFS (then pid).

## Current Session Notes

- Default branch: `main`.
- GitHub MCP unavailable; using local git push.
- Phase 0: `d663e72`
- User requested Phases 1–6 autonomously in one session.
