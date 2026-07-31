# Sample Test Cases (Live Demo)

Three hand-checked cases per algorithm. Use these during demos: enter the processes, run the algorithm, and confirm Gantt order + averages.

Legend: process = `(PID, Arrival, Burst[, Priority])`.

---

## FCFS

### TC-FCFS-1 — All arrive at time 0
**Input:** `(1,0,5), (2,0,3), (3,0,1)`  
**Gantt:** P1 [0–5], P2 [5–8], P3 [8–9]  
**Waiting:** 0, 5, 8 → **avg WT = 13/3 ≈ 4.33**  
**Turnaround:** 5, 8, 9 → **avg TAT = 22/3 ≈ 7.33**

### TC-FCFS-2 — Staggered arrivals
**Input:** `(1,0,4), (2,1,3), (3,2,2)`  
**Gantt:** P1 [0–4], P2 [4–7], P3 [7–9]  
**Waiting:** 0, 3, 5 → **avg WT = 8/3 ≈ 2.67**  
**Turnaround:** 4, 6, 7 → **avg TAT = 17/3 ≈ 5.67**

### TC-FCFS-3 — Idle gap
**Input:** `(1,0,2), (2,5,3)`  
**Gantt:** P1 [0–2], IDLE [2–5], P2 [5–8]  
**Waiting:** 0, 0 → **avg WT = 0**  
**Turnaround:** 2, 3 → **avg TAT = 2.5**

---

## SJF (non-preemptive)

### TC-SJF-1 — Staggered (classic)
**Input:** `(1,0,7), (2,2,4), (3,4,1), (4,5,4)`  
**Gantt:** P1 [0–7], P3 [7–8], P2 [8–12], P4 [12–16]  
**Waiting:** 0, 6, 3, 7 → **avg WT = 4**  
**Turnaround:** 7, 10, 4, 11 → **avg TAT = 8**

### TC-SJF-2 — Tie on burst (lower PID wins)
**Input:** `(2,0,3), (1,0,3)`  
**Gantt:** P1 [0–3], P2 [3–6]  
**avg WT = 1.5**, **avg TAT = 4.5**

### TC-SJF-3 — Short job already waiting
**Input:** `(1,0,8), (2,0,2), (3,0,4)`  
**Gantt:** P2 [0–2], P3 [2–6], P1 [6–14]  
**Waiting:** 6, 0, 2 → **avg WT = 8/3 ≈ 2.67**

---

## SRTF (SJF preemptive)

### TC-SRTF-1 — Mid-execution preemption
**Input:** `(1,0,8), (2,1,4), (3,2,9), (4,3,5)`  
**Gantt:** P1 [0–1], P2 [1–5], P4 [5–10], P1 [10–17], P3 [17–26]  
**Waiting:** 9, 0, 15, 2 → **avg WT = 6.5**  
**Turnaround:** 17, 4, 24, 7 → **avg TAT = 13**

### TC-SRTF-2 — No preemption needed
**Input:** `(1,0,2), (2,3,2)`  
**Gantt:** P1 [0–2], IDLE [2–3], P2 [3–5]  
**avg WT = 0**, **avg TAT = 2**

### TC-SRTF-3 — Equal remaining → lower PID
**Input:** `(1,0,4), (2,0,4)`  
**Gantt:** P1 [0–4], P2 [4–8]  
**avg WT = 2**, **avg TAT = 6**

---

## Priority (non-preemptive) — lower number = higher priority

### TC-PRIO-NP-1 — Basic ordering
**Input:** `(1,0,4,pri=2), (2,0,3,pri=1), (3,0,2,pri=3)`  
**Gantt:** P2 [0–3], P1 [3–7], P3 [7–9]  
**Waiting:** 3, 0, 7 → **avg WT ≈ 3.33**

### TC-PRIO-NP-2 — Equal priority → arrival then PID
**Input:** `(1,1,3,pri=1), (2,0,2,pri=1), (3,0,4,pri=1)`  
**Gantt:** P2 [0–2], P3 [2–6], P1 [6–9]  
**Waiting:** 5, 0, 2 → **avg WT ≈ 2.33**

### TC-PRIO-NP-3 — Late high-priority arrival (no preemption)
**Input:** `(1,0,5,pri=3), (2,2,2,pri=1)`  
**Gantt:** P1 [0–5], P2 [5–7]  
**Waiting:** 0, 3 → **avg WT = 1.5**

---

## Priority (preemptive)

### TC-PRIO-P-1 — Higher priority arrives mid-run
**Input:** `(1,0,5,pri=3), (2,2,2,pri=1)`  
**Gantt:** P1 [0–2], P2 [2–4], P1 [4–7]  
**Waiting:** 2, 0 → **avg WT = 1**  
**Turnaround:** 7, 2 → **avg TAT = 4.5**

### TC-PRIO-P-2 — No preemption (arrivals lower priority)
**Input:** `(1,0,4,pri=1), (2,1,3,pri=5)`  
**Gantt:** P1 [0–4], P2 [4–7]  
**avg WT = 1.5**

### TC-PRIO-P-3 — Three-way priority
**Input:** `(1,0,6,pri=3), (2,1,2,pri=1), (3,2,2,pri=2)`  
**Gantt:** P1 [0–1], P2 [1–3], P3 [3–5], P1 [5–10]  
**Waiting:** 4, 0, 1 → **avg WT ≈ 1.67**

---

## Round Robin

### TC-RR-1 — Quantum = 1
**Input:** `(1,0,3), (2,0,2), (3,0,1)`, **q=1**  
**Gantt:** P1 [0–1], P2 [1–2], P3 [2–3], P1 [3–4], P2 [4–5], P1 [5–6]  
**Waiting:** 3, 3, 2 → **avg WT ≈ 2.67**  
**Turnaround:** 6, 5, 3 → **avg TAT ≈ 4.67**

### TC-RR-2 — Quantum = 4 (staggered)
**Input:** `(1,0,5), (2,1,4), (3,2,2)`, **q=4**  
**Gantt:** P1 [0–4], P2 [4–8], P3 [8–10], P1 [10–11]  
**Waiting:** 6, 3, 6 → **avg WT = 5**  
**Turnaround:** 11, 7, 8 → **avg TAT ≈ 8.67**

### TC-RR-3 — Quantum larger than all bursts (behaves like FCFS)
**Input:** `(1,0,3), (2,1,2), (3,4,1)`, **q=10**  
**Gantt:** P1 [0–3], P2 [3–5], P3 [5–6]  
**Waiting:** 0, 2, 1 → **avg WT = 1**  
**Turnaround:** 3, 4, 2 → **avg TAT = 3**

---

## Suggested demo order

1. **FCFS TC-FCFS-3** — show IDLE gap clearly on the Gantt chart.  
2. **SRTF TC-SRTF-1** — talk through preemption when a shorter job arrives.  
3. **Priority TC-PRIO-P-1** — contrast with non-preemptive TC-PRIO-NP-3.  
4. **Round Robin TC-RR-1** then **TC-RR-3** — quantum effect vs FCFS-like behavior.  
5. Open **Compare All Algorithms** on the SRTF input set and point at the lowest avg waiting time.
