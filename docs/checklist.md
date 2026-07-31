# Pre-submission checklist

## Done in the repo

- [x] Process model with validation
- [x] FCFS, SJF, SRTF, Priority (NP + P), Round Robin
- [x] Metrics + cross-algorithm comparison helpers
- [x] Tkinter GUI: input form, Gantt chart, results table, comparison tab
- [x] Idle-gap rendering on Gantt charts
- [x] Deterministic tie-breaking (lower PID; priority → arrival → PID)
- [x] Unit tests (`pytest tests/`) — currently **39 passed**
- [x] Edge cases: empty list, single process, duplicate arrivals, identical bursts
- [x] README, report template, sample demo cases
- [x] No hardcoded absolute paths; `python src/main.py` entrypoint

## Still do manually

- [ ] Add teammate name in `README.md` and report Appendix A
- [ ] Capture screenshots into `screenshots/` (simulation Gantt, RR, SRTF preemption, comparison tab)
- [ ] Link screenshots in `README.md` and fill Section 6 of `docs/report_template.md`
- [ ] Write report prose (problem statement, conclusion, references with your course materials)
- [ ] Practice the live demo walkthrough below once end-to-end
- [ ] Confirm Tkinter works on the demo machine (`python -c "import tkinter"`)
- [ ] Zip / submit per your course instructions (include `README`, `src/`, `tests/`, `docs/`, screenshots)

## Demo-day walkthrough (≈8–10 minutes)

1. **Open the app** — `python src/main.py`. Point out process table + algorithm dropdown.
2. **FCFS + IDLE** — load `(1,0,2), (2,5,3)`. Run FCFS. Say: “When the CPU has nothing ready, we emit an explicit IDLE block so the Gantt stays honest.”
3. **Tie-breaking** — load three jobs at t=0 with equal burst `(1,0,4), (2,0,4), (3,0,4)`. Run SJF. Say: “Equal key → lower PID wins, so order is always P1, P2, P3.”
4. **SRTF preemption** — load TC-SRTF-1 from `docs/sample_test_cases.md`. Walk the Gantt: P1 starts, P2 preempts at t=1, etc.
5. **Priority contrast** — same processes as TC-PRIO-NP-3 vs TC-PRIO-P-1 to show non-preemptive vs preemptive.
6. **Round Robin** — TC-RR-1 (q=1) then TC-RR-3 (q=10 ≈ FCFS). Explain arrival ordering into the ready queue.
7. **Compare All** — keep the SRTF workload, open the comparison tab, Run Comparison. Call out the algorithm with lowest average waiting time.
8. **Tests** — optionally flash `pytest tests/ -v` (39 passed) for validation credibility.

### Talking points

- **Waiting time** = turnaround − burst; **response** = first start − arrival.
- **CPU utilization** uses timeline busy time / full span (IDLE lowers utilization).
- Priority starvation is acknowledged in code comments; aging is future work.
