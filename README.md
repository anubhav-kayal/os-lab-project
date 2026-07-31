# CPU Scheduling Simulator

Interactive desktop tool for exploring classic CPU scheduling algorithms. Build a process workload, run a scheduler, and inspect the execution timeline as a Gantt chart alongside waiting, turnaround, and response-time metrics. Compare every algorithm on the same input in one click.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Charts](https://img.shields.io/badge/charts-matplotlib-orange)
![Tests](https://img.shields.io/badge/tests-pytest-yellow)

## Features

- **Six schedulers**
  - FCFS (First Come First Served)
  - SJF — non-preemptive
  - SRTF — preemptive SJF
  - Priority — non-preemptive and preemptive (lower number = higher priority by default)
  - Round Robin with configurable time quantum
- **Gantt chart** rendered with matplotlib inside the Tkinter window (including IDLE gaps)
- **Per-process results table** with averages for waiting, turnaround, and response time
- **Compare All Algorithms** dashboard — same workload, side-by-side average waiting / turnaround bars
- **Deterministic tie-breaking** — lower PID wins; equal priority falls back to arrival order
- **Unit-tested** scheduling core (`pytest`)

## Screenshots

Drop demo captures into `screenshots/` and link them here:

| Simulation view | Comparison view |
| --- | --- |
| `screenshots/simulation.png` | `screenshots/comparison.png` |

## Requirements

- Python **3.11+** with Tkinter support
- `matplotlib`
- `pytest` (for running tests)

> On macOS, if `import tkinter` fails under a Homebrew/pyenv build, use a Framework Python that ships with Tcl/Tk, for example:
> `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`

## Install

```bash
git clone https://github.com/anubhav-kayal/os-lab-project.git
cd os-lab-project
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 src/main.py
```

1. Add processes (arrival time, burst time; priority when using Priority schedulers).
2. Choose an algorithm (enable time quantum for Round Robin).
3. Click **Run Simulation** to refresh the Gantt chart and results table.
4. Open **Compare All Algorithms** and click **Run Comparison** for a cross-scheduler chart.

## Test

```bash
python3 -m pytest tests/ -v
```

## Project layout

```
os-lab-project/
├── README.md
├── requirements.txt
├── plan.md                 # build plan / progress
├── agents.md               # agent workflow notes
├── src/
│   ├── main.py             # entrypoint
│   ├── models.py           # Process / PCB model
│   ├── metrics.py          # averages, util %, comparison helpers
│   ├── scheduler.py        # GUI → algorithm dispatch
│   ├── algorithms/         # FCFS, SJF/SRTF, Priority, Round Robin
│   └── gui/                # Tkinter UI, Gantt, comparison view
├── tests/                  # pytest suite
├── docs/
│   ├── report_template.md
│   └── sample_test_cases.md
└── screenshots/            # optional demo images
```

## Design overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  InputForm  │────▶│  scheduler   │────▶│  algorithm impl │
│  (Tkinter)  │     │  dispatch    │     │  + timeline     │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
                    ┌──────────────┐              │
                    │   metrics    │◀─────────────┤
                    └──────┬───────┘              │
                           │                      │
              ┌────────────┼────────────┐         │
              ▼            ▼            ▼         ▼
        ResultsTable   GanttChart   ComparisonView
```

Each scheduler returns `(processes, timeline)` where `timeline` is a list of `(pid | "IDLE", start, end)` segments. The GUI never mutates the user’s input objects — algorithms work on copies. Metrics (waiting, turnaround, response, CPU utilization, throughput) are derived from completed process fields and the timeline.

**Conventions**

- Idle CPU time appears explicitly as `IDLE` blocks on the Gantt chart.
- Tie-break: lower `pid` wins when arrival/burst/priority are equal.
- Priority default: smaller number = higher priority (`lower_is_higher=True`, configurable in code).

## Algorithms at a glance

| Algorithm | Preemptive? | Selection key |
| --- | --- | --- |
| FCFS | No | Earliest arrival, then PID |
| SJF | No | Shortest burst among ready |
| SRTF | Yes | Shortest remaining time |
| Priority (NP / P) | No / Yes | Priority, then arrival, then PID |
| Round Robin | Yes (quantum) | Ready queue / time slice |

## Authors

- Anubhav Kayal
- [Teammate name]

## License

Educational / personal project. Feel free to fork and adapt.
