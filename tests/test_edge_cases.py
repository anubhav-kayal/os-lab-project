"""Edge-case coverage for scheduling algorithms and metrics."""

from __future__ import annotations

import pytest

from models import Process
from algorithms.fcfs import fcfs_schedule
from algorithms.sjf import sjf_non_preemptive, sjf_preemptive
from algorithms.priority import priority_non_preemptive, priority_preemptive
from algorithms.round_robin import round_robin_schedule
from metrics import average_waiting_time, summarize
from scheduler import run_algorithm


ALL_RUNNERS = [
    ("FCFS", lambda ps: fcfs_schedule(ps)),
    ("SJF-NP", lambda ps: sjf_non_preemptive(ps)),
    ("SJF-P", lambda ps: sjf_preemptive(ps)),
    ("PRIO-NP", lambda ps: priority_non_preemptive(ps)),
    ("PRIO-P", lambda ps: priority_preemptive(ps)),
    ("RR", lambda ps: round_robin_schedule(ps, 2)),
]


def _prio(pid: int, arrival: int, burst: int, priority: int = 1) -> Process:
    return Process(pid, arrival, burst, priority=priority)


@pytest.mark.parametrize("name,runner", ALL_RUNNERS)
def test_empty_process_list(name, runner):
    """Empty input returns empty results (GUI disables Run for this case)."""
    result, timeline = runner([])
    assert result == []
    assert timeline == []


@pytest.mark.parametrize("name,runner", ALL_RUNNERS)
def test_single_process(name, runner):
    """A lone process runs immediately with zero waiting time."""
    procs = [_prio(1, 0, 5, priority=1)]
    result, timeline = runner(procs)
    by_pid = {p.pid: p for p in result}
    assert by_pid[1].waiting_time == 0
    assert by_pid[1].turnaround_time == 5
    assert by_pid[1].response_time == 0
    assert timeline == [(1, 0, 5)]


@pytest.mark.parametrize("name,runner", ALL_RUNNERS)
def test_duplicate_arrival_times(name, runner):
    """Multiple processes arriving at the same time stay deterministic."""
    procs = [
        _prio(2, 0, 4, priority=2),
        _prio(1, 0, 3, priority=1),
        _prio(3, 0, 2, priority=3),
    ]
    result, timeline = runner(procs)
    assert len(result) == 3
    assert timeline[0][1] == 0
    assert all(p.completion_time is not None for p in result)
    # No IDLE when everyone arrives at 0 with positive bursts.
    assert all(seg[0] != "IDLE" for seg in timeline)
    assert average_waiting_time(result) >= 0


def test_identical_burst_times_tie_break_fcfs_and_sjf():
    """Identical bursts: lower pid wins under FCFS arrival-tie and SJF burst-tie."""
    procs = [
        Process(3, 0, 4),
        Process(1, 0, 4),
        Process(2, 0, 4),
    ]
    fcfs_result, fcfs_tl = fcfs_schedule(procs)
    assert [p.pid for p in fcfs_result] == [1, 2, 3]
    assert [seg[0] for seg in fcfs_tl] == [1, 2, 3]

    sjf_result, sjf_tl = sjf_non_preemptive(procs)
    assert [p.pid for p in sjf_result] == [1, 2, 3]
    assert [seg[0] for seg in sjf_tl] == [1, 2, 3]


def test_identical_priority_falls_back_to_arrival_then_pid():
    """Stress equal-priority scheduling with identical bursts."""
    procs = [
        Process(2, 0, 3, priority=5),
        Process(1, 0, 3, priority=5),
        Process(3, 1, 3, priority=5),
    ]
    result, timeline = priority_non_preemptive(procs)
    assert [p.pid for p in result] == [1, 2, 3]
    assert timeline == [(1, 0, 3), (2, 3, 6), (3, 6, 9)]


def test_scheduler_dispatch_unknown_algorithm():
    with pytest.raises(ValueError, match="Unknown algorithm"):
        run_algorithm("Not Real", [Process(1, 0, 1)])


def test_summarize_single_process_with_late_arrival():
    """Single process arriving after time 0 produces a leading IDLE gap."""
    result, timeline = fcfs_schedule([Process(1, 2, 4)])
    stats = summarize(result, timeline)
    assert stats["avg_waiting_time"] == 0
    assert stats["avg_turnaround_time"] == 4
    assert timeline == [("IDLE", 0, 2), (1, 2, 6)]
    assert stats["cpu_utilization"] == pytest.approx((4 / 6) * 100)
