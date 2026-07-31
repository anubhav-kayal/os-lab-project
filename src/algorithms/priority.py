"""Priority scheduling (non-preemptive and preemptive).

NOTE ON STARVATION:
Priority scheduling can starve low-priority processes if high-priority work
keeps arriving. Aging (gradually boosting waiting processes) is a common fix
but is intentionally not implemented here — we only acknowledge the issue.
"""

from __future__ import annotations

from models import Process, ScheduleResult

from .common import (
    append_timeline,
    finalize_process,
    mark_start,
    prepare_processes,
)


def _priority_key(process: Process, lower_is_higher: bool) -> tuple:
    """Sort key: priority first, then arrival, then pid (FCFS-style tie-break)."""
    if process.priority is None:
        raise ValueError(
            f"Process {process.pid} is missing priority required for priority scheduling"
        )
    # lower_is_higher=True → smaller priority value sorts first
    pri = process.priority if lower_is_higher else -process.priority
    return (pri, process.arrival_time, process.pid)


def priority_non_preemptive(
    processes: list[Process],
    *,
    lower_is_higher: bool = True,
) -> ScheduleResult:
    """Non-preemptive priority scheduling.

    Args:
        processes: Input processes (must include priority on each).
        lower_is_higher: If True (default), smaller priority numbers win
            (standard OS convention). If False, larger numbers win.

    Returns:
        (execution-ordered completed processes, Gantt timeline).
    """
    jobs = prepare_processes(processes)
    if not jobs:
        return [], []

    pending = list(jobs)
    timeline: list = []
    current_time = 0
    execution_order: list[Process] = []
    done: set[int] = set()
    n = len(pending)

    while len(done) < n:
        ready = [
            p
            for p in pending
            if p.pid not in done and p.arrival_time <= current_time
        ]
        if not ready:
            next_arrival = min(
                p.arrival_time for p in pending if p.pid not in done
            )
            append_timeline(timeline, "IDLE", current_time, next_arrival)
            current_time = next_arrival
            continue

        selected = min(ready, key=lambda p: _priority_key(p, lower_is_higher))
        mark_start(selected, current_time)
        start = current_time
        end = start + selected.burst_time
        append_timeline(timeline, selected.pid, start, end)
        finalize_process(selected, end)
        current_time = end
        execution_order.append(selected)
        done.add(selected.pid)

    return execution_order, timeline


def priority_preemptive(
    processes: list[Process],
    *,
    lower_is_higher: bool = True,
) -> ScheduleResult:
    """Preemptive priority scheduling.

    Re-evaluates at arrivals and completions. A newly arrived higher-priority
    process preempts the running process. Equal priority falls back to
    arrival_time then pid (FCFS-style).

    Args:
        processes: Input processes with priority set.
        lower_is_higher: Priority direction (default: lower number = higher priority).

    Returns:
        (completed processes sorted by pid, Gantt timeline).
    """
    jobs = prepare_processes(processes)
    if not jobs:
        return [], []

    by_pid = {p.pid: p for p in jobs}
    arrivals = sorted(jobs, key=lambda p: (p.arrival_time, p.pid))
    timeline: list = []
    current_time = 0
    completed = 0
    n = len(jobs)
    ready: list[Process] = []
    arrival_idx = 0
    running: Process | None = None

    def enqueue_arrivals(up_to: int) -> None:
        nonlocal arrival_idx
        while arrival_idx < n and arrivals[arrival_idx].arrival_time <= up_to:
            ready.append(arrivals[arrival_idx])
            arrival_idx += 1

    def best(candidates: list[Process]) -> Process:
        return min(candidates, key=lambda p: _priority_key(p, lower_is_higher))

    while completed < n:
        enqueue_arrivals(current_time)

        if running is None and not ready:
            next_arrival = arrivals[arrival_idx].arrival_time
            append_timeline(timeline, "IDLE", current_time, next_arrival)
            current_time = next_arrival
            continue

        if running is None:
            running = best(ready)
            ready.remove(running)
            mark_start(running, current_time)

        finish_time = current_time + running.remaining_time
        next_arrival_time = (
            arrivals[arrival_idx].arrival_time if arrival_idx < n else None
        )

        if next_arrival_time is not None and next_arrival_time < finish_time:
            run_end = next_arrival_time
            ran = run_end - current_time
            append_timeline(timeline, running.pid, current_time, run_end)
            running.remaining_time -= ran
            current_time = run_end
            enqueue_arrivals(current_time)
            candidate = best(ready + [running])
            if candidate is not running:
                ready.append(running)
                running = candidate
                ready.remove(candidate)
                mark_start(running, current_time)
        else:
            append_timeline(timeline, running.pid, current_time, finish_time)
            finalize_process(running, finish_time)
            current_time = finish_time
            completed += 1
            running = None

    return sorted(by_pid.values(), key=lambda p: p.pid), timeline
