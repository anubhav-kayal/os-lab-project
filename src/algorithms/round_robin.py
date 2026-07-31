"""Round Robin scheduling algorithm."""

from __future__ import annotations

from collections import deque

from models import Process, ScheduleResult

from .common import (
    append_timeline,
    finalize_process,
    mark_start,
    prepare_processes,
)


def round_robin_schedule(
    processes: list[Process],
    time_quantum: int,
) -> ScheduleResult:
    """Schedule processes using Round Robin with a fixed time quantum.

    Ready-queue rule for arrivals during a quantum:
    new arrivals are enqueued after processes already waiting, but *before*
    the just-preempted process is re-appended. This matches the common textbook
    RR arrival ordering used in OS courses.

    Args:
        processes: Input process list (not mutated).
        time_quantum: Positive slice length granted to each ready process.

    Returns:
        (completed processes sorted by pid, Gantt timeline).

    Raises:
        ValueError: If time_quantum is not a positive integer.
    """
    if not isinstance(time_quantum, int) or isinstance(time_quantum, bool):
        raise ValueError(
            f"time_quantum must be a positive integer, got {type(time_quantum).__name__}"
        )
    if time_quantum <= 0:
        raise ValueError(f"time_quantum must be positive, got {time_quantum}")

    jobs = prepare_processes(processes)
    if not jobs:
        return [], []

    by_pid = {p.pid: p for p in jobs}
    arrivals = sorted(jobs, key=lambda p: (p.arrival_time, p.pid))
    n = len(jobs)
    timeline: list = []
    ready: deque[Process] = deque()
    current_time = 0
    completed = 0
    arrival_idx = 0

    def enqueue_arrivals(up_to: int) -> None:
        """Add all processes that have arrived by time up_to to the ready queue."""
        nonlocal arrival_idx
        while arrival_idx < n and arrivals[arrival_idx].arrival_time <= up_to:
            ready.append(arrivals[arrival_idx])
            arrival_idx += 1

    # Start at first arrival if needed
    if arrivals[0].arrival_time > 0:
        append_timeline(timeline, "IDLE", 0, arrivals[0].arrival_time)
        current_time = arrivals[0].arrival_time

    enqueue_arrivals(current_time)

    while completed < n:
        if not ready:
            # Idle until next arrival
            next_arrival = arrivals[arrival_idx].arrival_time
            append_timeline(timeline, "IDLE", current_time, next_arrival)
            current_time = next_arrival
            enqueue_arrivals(current_time)
            continue

        process = ready.popleft()
        mark_start(process, current_time)

        slice_len = min(time_quantum, process.remaining_time)
        start = current_time
        end = start + slice_len

        # Arrivals that happen *during* this slice (after start, up to end)
        # are queued before the preempted process re-enters.
        # Processes arriving exactly at `start` were already enqueued.
        append_timeline(timeline, process.pid, start, end)
        process.remaining_time -= slice_len
        current_time = end

        # Enqueue arrivals in (start, end] — i.e. up to current_time inclusive
        # but excluding those already queued at start. enqueue_arrivals handles
        # arrival_time <= current_time and skips already-consumed arrivals.
        enqueue_arrivals(current_time)

        if process.remaining_time == 0:
            finalize_process(process, current_time)
            completed += 1
        else:
            # Preempted: re-enter after any new arrivals from this quantum
            ready.append(process)

    return sorted(by_pid.values(), key=lambda p: p.pid), timeline
