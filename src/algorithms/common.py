"""Shared helpers for CPU scheduling algorithms."""

from __future__ import annotations

from models import Process, TimelineEntry


def prepare_processes(processes: list[Process]) -> list[Process]:
    """Return working copies of processes for a scheduling run."""
    if not processes:
        return []
    copies = [p.copy() for p in processes]
    pids = [p.pid for p in copies]
    if len(pids) != len(set(pids)):
        raise ValueError("Duplicate process ids are not allowed")
    return copies


def append_timeline(
    timeline: list[TimelineEntry],
    pid: int | str,
    start: int,
    end: int,
) -> None:
    """Append a timeline segment, merging adjacent identical blocks."""
    if end < start:
        raise ValueError(f"Invalid timeline segment: end ({end}) < start ({start})")
    if end == start:
        return
    if timeline and timeline[-1][0] == pid and timeline[-1][2] == start:
        prev_pid, prev_start, _ = timeline[-1]
        timeline[-1] = (prev_pid, prev_start, end)
    else:
        timeline.append((pid, start, end))


def mark_start(process: Process, current_time: int) -> None:
    """Record first CPU grant time if not already set."""
    if process.start_time is None:
        process.start_time = current_time


def finalize_process(process: Process, completion_time: int) -> None:
    """Set completion time and derive waiting/turnaround/response metrics."""
    process.completion_time = completion_time
    process.remaining_time = 0
    process.finalize_times()
