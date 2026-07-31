# CPU Scheduling Simulator — Build Plan

**Project:** CPU Scheduling Simulator with Gantt Charts  
**Course:** Operating Systems Lab Mini-Project (30 marks)  
**Repo:** https://github.com/anubhav-kayal/os-lab-project  
**Stack:** Python 3.11+, Tkinter, matplotlib (+ pytest for tests)

## Global Rules

1. Only stdlib + tkinter + matplotlib (no heavy frameworks).
2. Follow the folder structure under `src/`, `tests/`, `docs/`, `screenshots/`.
3. Commit discipline:
   - After ~150 lines of new/changed code (running total), stop, run tests, commit.
   - Prefer GitHub MCP when available; otherwise local `git` + `git push`.
   - Message format: `"Phase X: <short description>"`.
   - Never combine unrelated phases in one commit.
   - Before each commit, list files being committed.
   - Batch all files for a phase-step into ONE commit.
   - Never commit `__pycache__/`, `.DS_Store`, `*.pyc`, `venv/`, `.pytest_cache/`.
   - If a phase is under 150 lines, still commit at end of phase.
4. Work on feature branches per phase, then merge/push to `main`.
5. After each phase: summarize, show how to run/test, commit+push, then wait for **"continue"** unless told to run phases autonomously.

## Phases

| Phase | Title | Commit message |
|------:|-------|----------------|
| 0 | Project scaffolding | Phase 0: project scaffolding and repo setup |
| 1 | Core Process data model | Phase 1: core Process data model |
| 2 | FCFS + tests | Phase 2: implement FCFS scheduling algorithm and unit tests |
| 3 | SJF non-preemptive + SRTF + tests | Phase 3: implement SJF (non-preemptive + preemptive/SRTF) with tests |
| 4 | Priority non-preemptive + preemptive + tests | Phase 4: implement Priority scheduling (non-preemptive + preemptive) with tests |
| 5 | Round Robin + tests | Phase 5: implement Round Robin scheduling with tests |
| 6 | Metrics module + tests | Phase 6: metrics calculation module with tests |
| 7 | GUI input form | Phase 7: GUI input form for process entry and algorithm selection |
| 8 | Gantt chart | Phase 8: Gantt chart rendering with matplotlib embedded in Tkinter |
| 9 | Results table + comparison dashboard | Phase 9: results table and cross-algorithm comparison dashboard |
| 10 | Edge cases, polish, full pytest | Phase 10: edge case handling, polish, full test suite passing |
| 11 | Docs / README / report template | Phase 11: documentation, README, and report template |
| 12 | Final review + checklist | Phase 12: final polish and pre-submission checklist |

## Progress Log

- [x] Phase 0 — `d663e72` on `main` + `phase-0-scaffolding`
- [x] Phase 1 — `c9e5904` on `main` + `phase-1-models`
- [x] Phase 2
- [x] Phase 3
- [x] Phase 4
- [ ] Phase 5
- [ ] Phase 6
- [ ] Phase 7
- [ ] Phase 8
- [ ] Phase 9
- [ ] Phase 10
- [ ] Phase 11
- [ ] Phase 12
