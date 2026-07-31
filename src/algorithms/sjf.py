"""SJF (Shortest Job First) and SRTF (preemptive SJF) scheduling."""

from __future__ import annotations

from models import Process, ScheduleResult

from .common import (
    append_timeline,
    finalize_process,
    mark_start,
    prepare_processes,
)


def sjf_non_preemptive(processes: list[Process]) -> ScheduleResult:
    """Schedule using non-preemptive Shortest Job First.

    At each scheduling decision, among arrived ready processes, pick the
    shortest burst_time. Ties break to lower pid.

    Args:
        processes: Input process list (not mutated).

    Returns:
        (completed processes in completion/execution order, Gantt timeline).
    """
    jobs = prepare_processes(processes)
    if not jobs:
        return [], []

    pending = sorted(jobs, key=lambda p: (p.arrival_time, p.pid))
    timeline: list = []
    current_time = 0
    execution_order: list[Process] = []
    completed = 0
    n = len(pending)
    done = set()

    while completed < n:
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

        selected = min(ready, key=lambda p: (p.burst_time, p.pid))
        mark_start(selected, current_time)
        start = current_time
        end = start + selected.burst_time
        append_timeline(timeline, selected.pid, start, end)
        finalize_process(selected, end)
        current_time = end
        execution_order.append(selected)
        done.add(selected.pid)
        completed += 1

    return execution_order, timeline


def sjf_preemptive(processes: list[Process]) -> ScheduleResult:
    """Schedule using preemptive SJF (Shortest Remaining Time First / SRTF).

    At every arrival or completion event, the ready process with the smallest
    remaining_time runs. Ties break to lower pid.

    Args:
        processes: Input process list (not mutated).

    Returns:
        (completed processes sorted by pid for stable reporting, Gantt timeline).
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

    while completed < n:
        enqueue_arrivals(current_time)

        if running is None and not ready:
            # Jump to next arrival
            next_arrival = arrivals[arrival_idx].arrival_time
            append_timeline(timeline, "IDLE", current_time, next_arrival)
            current_time = next_arrival
            continue

        if running is None:
            running = min(ready, key=lambda p: (p.remaining_time, p.pid))
            ready.remove(running)
            mark_start(running, current_time)

        # Next event: either next arrival that could preempt, or this job finishes
        finish_time = current_time + running.remaining_time
        next_arrival_time = (
            arrivals[arrival_idx].arrival_time if arrival_idx < n else None
        )

        if next_arrival_time is not None and next_arrival_time < finish_time:
            # Run until arrival, then re-evaluate
            run_end = next_arrival_time
            ran = run_end - current_time
            append_timeline(timeline, running.pid, current_time, run_end)
            running.remaining_time -= ran
            current_time = run_end
            enqueue_arrivals(current_time)
            # Preempt if a shorter (or equal with lower pid) job is ready
            candidate = min(
                ready + [running],
                key=lambda p: (p.remaining_time, p.pid),
            )
            if candidate is not running:
                ready.append(running)
                running = candidate
                ready.remove(candidate)
                mark_start(running, current_time)
        else:
            # Finish current process
            append_timeline(timeline, running.pid, current_time, finish_time)
            finalize_process(running, finish_time)
            current_time = finish_time
            completed += 1
            running = None

    # Return processes in pid order for stable metrics assertions
    completed_list = sorted(by_pid.values(), key=lambda p: p.pid)
    return completed_list, timeline
