"""Unit tests for priority scheduling."""

from __future__ import annotations

from models import Process
from algorithms.priority import priority_non_preemptive, priority_preemptive


def _by_pid(processes: list[Process]) -> dict[int, Process]:
    return {p.pid: p for p in processes}


def test_priority_non_preemptive_basic():
    """Lower number = higher priority (default).

    P1(0,4,pri=2), P2(0,3,pri=1), P3(0,2,pri=3)
    Order by priority: P2, P1, P3
    Timeline: P2 [0-3], P1 [3-7], P3 [7-9]
    Waiting: P2=0, P1=3, P3=7
    """
    procs = [
        Process(1, 0, 4, priority=2),
        Process(2, 0, 3, priority=1),
        Process(3, 0, 2, priority=3),
    ]
    result, timeline = priority_non_preemptive(procs)
    by_pid = _by_pid(result)

    assert [p.pid for p in result] == [2, 1, 3]
    assert timeline == [(2, 0, 3), (1, 3, 7), (3, 7, 9)]
    assert by_pid[2].waiting_time == 0
    assert by_pid[1].waiting_time == 3
    assert by_pid[3].waiting_time == 7


def test_priority_equal_falls_back_to_arrival_then_pid():
    """Equal priority → FCFS by arrival_time, then lower pid.

    P1(1,3,pri=1), P2(0,2,pri=1), P3(0,4,pri=1)
    At t=0 ready: P2 and P3 (equal pri). Earlier arrival both 0 → lower pid P2.
    Then P3, then P1.
    Timeline: P2 [0-2], P3 [2-6], P1 [6-9]
    """
    procs = [
        Process(1, 1, 3, priority=1),
        Process(2, 0, 2, priority=1),
        Process(3, 0, 4, priority=1),
    ]
    result, timeline = priority_non_preemptive(procs)
    assert [p.pid for p in result] == [2, 3, 1]
    assert timeline == [(2, 0, 2), (3, 2, 6), (1, 6, 9)]


def test_priority_preemptive_higher_arrives():
    """Higher-priority arrival preempts the running process.

    P1(0,5,pri=3), P2(2,2,pri=1)
    P1 runs [0-2], P2 preempts [2-4], P1 resumes [4-7]
    Waiting: P1=2, P2=0
    Turnaround: P1=7, P2=2
    """
    procs = [
        Process(1, 0, 5, priority=3),
        Process(2, 2, 2, priority=1),
    ]
    result, timeline = priority_preemptive(procs)
    by_pid = _by_pid(result)

    assert timeline == [(1, 0, 2), (2, 2, 4), (1, 4, 7)]
    assert by_pid[1].waiting_time == 2
    assert by_pid[1].turnaround_time == 7
    assert by_pid[1].response_time == 0
    assert by_pid[2].waiting_time == 0
    assert by_pid[2].turnaround_time == 2


def test_priority_higher_number_wins_when_configured():
    """lower_is_higher=False → larger priority value is preferred."""
    procs = [
        Process(1, 0, 2, priority=1),
        Process(2, 0, 2, priority=5),
    ]
    result, _ = priority_non_preemptive(procs, lower_is_higher=False)
    assert [p.pid for p in result] == [2, 1]
