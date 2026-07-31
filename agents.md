# Agent Notes — CPU Scheduling Simulator

## Mission
Build a CPU Scheduling Simulator with Gantt Charts following `plan.md`.

## Stack
Python 3.11+, Tkinter, matplotlib, pytest. No heavy frameworks.

## Workflow
- Feature branches per phase; merge to `main` after each phase commit.
- Commit message: `Phase X: <short description>`.
- GitHub MCP unavailable here → use `git push`.
- Run `pytest tests/ -v` before commits once tests exist.

## Scheduler return shape
`(list[Process], timeline)` where timeline entries are `(pid|"IDLE", start, end)`.

## Tie-breaking
Lower pid wins; equal priority → arrival then pid.

## Session progress
- Phases 0–6 complete (algorithms + metrics + unit tests).
- Next: Phase 7 GUI input form — wait for user **continue**.
