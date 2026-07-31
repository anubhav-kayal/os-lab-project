"""Algorithms package: FCFS, SJF/SRTF, Priority, and Round Robin schedulers."""

from __future__ import annotations

from .fcfs import fcfs_schedule
from .sjf import sjf_non_preemptive, sjf_preemptive
from .priority import priority_non_preemptive, priority_preemptive
from .round_robin import round_robin_schedule

__all__ = [
    "fcfs_schedule",
    "sjf_non_preemptive",
    "sjf_preemptive",
    "priority_non_preemptive",
    "priority_preemptive",
    "round_robin_schedule",
]
