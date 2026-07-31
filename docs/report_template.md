# Project Report Template

Use this skeleton for the written report. Replace bracketed placeholders after capturing screenshots and finalizing wording.

---

## 1. Problem Statement

[Describe the problem: understanding and comparing CPU scheduling algorithms is abstract without visualization. This project provides an interactive simulator with Gantt charts and quantitative metrics.]

**Example draft:**
Operating systems rely on CPU scheduling to decide which ready process runs next. Students and practitioners often study algorithms such as FCFS, SJF, Priority, and Round Robin from textbooks, but hand-drawn timelines make it hard to compare trade-offs quickly. This project builds a desktop simulator that accepts a process workload, runs a chosen algorithm, visualizes the timeline, and reports waiting / turnaround / response metrics — including a cross-algorithm comparison on the same input.

---

## 2. Objectives

- [ ] Implement FCFS, SJF (non-preemptive), SRTF, Priority (NP + P), and Round Robin.
- [ ] Provide a GUI for process entry, algorithm selection, and time quantum.
- [ ] Render a proportional Gantt chart (with IDLE gaps).
- [ ] Compute per-process and average scheduling metrics.
- [ ] Compare all algorithms on one workload via charts.
- [ ] Validate correctness with automated unit tests and sample demo cases.

---

## 3. System Design

### 3.1 Architecture

[Paste or redraw the design overview from README.md: InputForm → scheduler dispatch → algorithm → metrics → Gantt / Results / Comparison.]

### 3.2 Modules

| Module | Responsibility |
| --- | --- |
| `models.py` | Process / PCB data model and validation |
| `algorithms/*` | Scheduling implementations + timeline |
| `metrics.py` | Averages, CPU utilization, throughput, comparison |
| `scheduler.py` | Name → algorithm dispatch for the GUI |
| `gui/*` | Tkinter UI, Gantt, results table, comparison |

### 3.3 Data contracts

- Input: list of `Process(pid, arrival_time, burst_time, priority?)`
- Output: `(list[Process], timeline)` where timeline entries are `(pid|"IDLE", start, end)`

---

## 4. Algorithm / Pseudocode

### 4.1 FCFS

```
sort processes by (arrival_time, pid)
time ← 0
for each process p:
  if time < p.arrival: record IDLE[time, p.arrival]; time ← p.arrival
  run p for burst_time; update start/completion/waiting/turnaround/response
```

### 4.2 SJF (non-preemptive) / SRTF

```
# Non-preemptive: among ready jobs, pick min(burst, pid)
# SRTF: at each arrival/completion, pick min(remaining, pid); preempt if needed
```

[Expand with the exact event-driven loop used in `sjf.py`.]

### 4.3 Priority

```
# lower number = higher priority (default)
# among ready: min(priority, arrival, pid)
# preemptive variant re-evaluates on arrivals
# NOTE: starvation of low-priority jobs is possible; aging not implemented
```

### 4.4 Round Robin

```
ready ← deque
on quantum expiry: enqueue arrivals during the slice, then re-append preempted process
```

---

## 5. Implementation

- Language: Python 3.11+
- GUI: Tkinter
- Charts: matplotlib (`FigureCanvasTkAgg`)
- Tests: pytest

**Key implementation notes**

- Algorithms operate on process copies (`Process.copy()`), so the form state stays clean.
- Timeline segments merge adjacent identical PIDs for cleaner Gantt blocks.
- Comparison view runs every algorithm on the current process set and charts avg waiting / turnaround.

[Add 1–2 paragraphs on any challenges: RR arrival ordering, IDLE handling, Tkinter + matplotlib embedding.]

---

## 6. Screenshots and Results

Insert images from `screenshots/` after the live demo.

### 6.1 FCFS run

![FCFS](../screenshots/fcfs.png)
[Briefly describe the process set and observed avg WT / TAT.]

### 6.2 SRTF preemption

![SRTF](../screenshots/srtf.png)

### 6.3 Round Robin

![RR](../screenshots/rr.png)

### 6.4 Comparison dashboard

![Compare](../screenshots/comparison.png)
[State which algorithm had the lowest average waiting time on your demo set.]

---

## 7. Testing and Validation

- Automated: `pytest tests/ -v` (FCFS, SJF, Priority, RR, metrics, edge cases).
- Manual: cases in `docs/sample_test_cases.md`.

| Area | Coverage |
| --- | --- |
| Correct waiting / turnaround | Hand-calculated asserts in unit tests |
| IDLE gaps | FCFS / late-arrival cases |
| Preemption | SRTF + Priority preemptive tests |
| RR quantum edge | q=1, q=4, q > all bursts |
| Edge cases | Empty list, single process, duplicate arrivals, identical bursts |

[Paste a pytest summary screenshot or count: e.g. 39 passed.]

---

## 8. Conclusion and Future Enhancements

**Conclusion**
[Summarize: simulator successfully visualizes and compares classic CPU schedulers with validated metrics.]

**Future enhancements**

- Priority aging to mitigate starvation
- Multilevel queue / feedback scheduling
- Export Gantt chart and metrics to PNG/CSV
- Animated step-through of the timeline
- Dark theme / accessibility pass on the GUI

---

## 9. References

1. Silberschatz, Galvin, Gagne — *Operating System Concepts* (CPU scheduling chapters).
2. Tanenbaum, Bos — *Modern Operating Systems*.
3. Python documentation — [tkinter](https://docs.python.org/3/library/tkinter.html), [asyncio N/A].
4. Matplotlib documentation — embedding in Tkinter (`FigureCanvasTkAgg`).
5. Course lecture notes on CPU scheduling (add your institution’s materials).

---

## Appendix A — Team

| Name | Role |
| --- | --- |
| Anubhav Kayal | [e.g. algorithms + metrics] |
| [Teammate] | [e.g. GUI + documentation] |

## Appendix B — How to run (for examiners)

```bash
pip install -r requirements.txt
python src/main.py
pytest tests/ -v
```
