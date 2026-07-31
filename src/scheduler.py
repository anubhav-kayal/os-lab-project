"""Algorithm dispatch helpers for the GUI."""

from __future__ import annotations

from typing import Optional

from models import Process, ScheduleResult
from algorithms.fcfs import fcfs_schedule
from algorithms.sjf import sjf_non_preemptive, sjf_preemptive
from algorithms.priority import priority_non_preemptive, priority_preemptive
from algorithms.round_robin import round_robin_schedule


def run_algorithm(
    algorithm_name: str,
    processes: list[Process],
    time_quantum: Optional[int] = None,
) -> ScheduleResult:
    """Run the named scheduling algorithm and return (processes, timeline).

    Args:
        algorithm_name: Display name from the GUI dropdown.
        processes: Input process list.
        time_quantum: Required when algorithm_name is Round Robin.

    Returns:
        ScheduleResult from the selected algorithm.

    Raises:
        ValueError: For unknown algorithms or missing Round Robin quantum.
    """
    if algorithm_name == "FCFS":
        return fcfs_schedule(processes)
    if algorithm_name == "SJF (non-preemptive)":
        return sjf_non_preemptive(processes)
    if algorithm_name == "SJF (preemptive / SRTF)":
        return sjf_preemptive(processes)
    if algorithm_name == "Priority (non-preemptive)":
        return priority_non_preemptive(processes)
    if algorithm_name == "Priority (preemptive)":
        return priority_preemptive(processes)
    if algorithm_name == "Round Robin":
        if time_quantum is None:
            raise ValueError("Round Robin requires a time quantum.")
        return round_robin_schedule(processes, time_quantum)
    raise ValueError(f"Unknown algorithm: {algorithm_name}")
