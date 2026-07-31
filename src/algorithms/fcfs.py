"""FCFS (First Come First Served) scheduling algorithm."""

from __future__ import annotations

from models import Process, ScheduleResult

from .common import (
    append_timeline,
    finalize_process,
    mark_start,
    prepare_processes,
)


def fcfs_schedule(processes: list[Process]) -> ScheduleResult:
    """Schedule processes using non-preemptive First Come First Served.

    Processes are ordered by arrival_time ascending, with lower pid breaking
    ties (stable, deterministic). Idle gaps are recorded as ("IDLE", start, end)
    when the CPU waits for the next arrival.

    Args:
        processes: Input process list (not mutated; working copies are used).

    Returns:
        A tuple of (completed processes in execution order, Gantt timeline).
    """
    ready = prepare_processes(processes)
    if not ready:
        return [], []

    ready.sort(key=lambda p: (p.arrival_time, p.pid))
    timeline: list = []
    current_time = 0
    execution_order: list[Process] = []

    for process in ready:
        if current_time < process.arrival_time:
            append_timeline(timeline, "IDLE", current_time, process.arrival_time)
            current_time = process.arrival_time

        mark_start(process, current_time)
        start = current_time
        end = start + process.burst_time
        append_timeline(timeline, process.pid, start, end)
        finalize_process(process, end)
        current_time = end
        execution_order.append(process)

    return execution_order, timeline
