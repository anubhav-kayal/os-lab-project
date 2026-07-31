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
   - Prefer GitHub MCP (`push_files` / `create_or_update_file`) when available; otherwise use local `git` + `git push` so commits still land on GitHub.
   - Message format: `"Phase X: <short description>"`.
   - Never combine unrelated phases in one commit.
   - Before each commit, list files being committed.
   - Batch all files for a phase-step into ONE commit.
   - Never commit `__pycache__/`, `.DS_Store`, `*.pyc`, `venv/`, `.pytest_cache/`.
   - If a phase is under 150 lines, still commit at end of phase.
4. Work on feature branches per phase (or phase group), then merge/push to default branch.
5. After each phase: summarize, show how to run/test, commit+push, then **wait for "continue"** unless told to run all phases autonomously.

## Target Structure

```
os-lab-project/
  README.md
  requirements.txt
  plan.md
  agents.md
  .gitignore
  src/
    models.py
    algorithms/
      fcfs.py
      sjf.py
      priority.py
      round_robin.py
    metrics.py
    gui/
      app.py
      input_form.py
      gantt_chart.py
      comparison_view.py
    main.py
  tests/
    test_fcfs.py
    test_sjf.py
    test_priority.py
    test_round_robin.py
    test_metrics.py
  docs/
    report_template.md
    sample_test_cases.md
  screenshots/
    .gitkeep
```

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

### Phase details (summary)

- **0:** Folders, stub files, `requirements.txt`, `.gitignore`, starter README.
- **1:** `Process` dataclass with validation + `__repr__`.
- **2:** `fcfs_schedule` → processes + timeline (incl. IDLE); ≥3 tests.
- **3:** `sjf_non_preemptive`, `sjf_preemptive` (SRTF); tie-break lower pid.
- **4:** Priority scheduling both modes; lower number = higher priority (configurable); starvation note in comments.
- **5:** Round Robin with deque; arrival ordering during quantum; quantum edge cases.
- **6:** Averages, CPU util %, throughput, `compare_algorithms`.
- **7:** Tkinter input form + wire to `app.py` (console print for now).
- **8:** matplotlib Gantt in Tkinter; wire Run Simulation to chart.
- **9:** Treeview results + Compare All Algorithms bar chart.
- **10:** Empty list / duplicates / single process / identical bursts; full pytest; docstrings.
- **11:** Full README, report skeleton (9 sections), sample test cases for demo.
- **12:** Consistency pass, launch check, manual checklist, demo walkthrough.

## Progress Log

- [x] Phase 0 — scaffolding committed (see agents.md for commit SHA)
- [ ] Phase 1
- [ ] Phase 2
- [ ] Phase 3
- [ ] Phase 4
- [ ] Phase 5
- [ ] Phase 6
- [ ] Phase 7
- [ ] Phase 8
- [ ] Phase 9
- [ ] Phase 10
- [ ] Phase 11
- [ ] Phase 12
