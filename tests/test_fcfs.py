"""Unit tests for FCFS scheduling.

Hand-calculated expected values are documented in comments per case.
"""

from __future__ import annotations

from models import Process
from algorithms.fcfs import fcfs_schedule


def _by_pid(processes: list[Process]) -> dict[int, Process]:
    return {p.pid: p for p in processes}


def test_fcfs_all_arrive_at_zero():
    """All arrive at t=0 → run in pid order.

    P1(0,5), P2(0,3), P3(0,1)
    Order: P1 [0-5], P2 [5-8], P3 [8-9]
    Waiting:  P1=0, P2=5, P3=8  avg=13/3
    Turnaround: P1=5, P2=8, P3=9
    Response: same as waiting for non-preemptive FCFS.
    """
    procs = [
        Process(1, 0, 5),
        Process(2, 0, 3),
        Process(3, 0, 1),
    ]
    result, timeline = fcfs_schedule(procs)
    by_pid = _by_pid(result)

    assert [p.pid for p in result] == [1, 2, 3]
    assert timeline == [(1, 0, 5), (2, 5, 8), (3, 8, 9)]

    assert by_pid[1].waiting_time == 0
    assert by_pid[1].turnaround_time == 5
    assert by_pid[1].response_time == 0

    assert by_pid[2].waiting_time == 5
    assert by_pid[2].turnaround_time == 8
    assert by_pid[2].response_time == 5

    assert by_pid[3].waiting_time == 8
    assert by_pid[3].turnaround_time == 9
    assert by_pid[3].response_time == 8


def test_fcfs_staggered_arrivals():
    """Staggered arrivals without idle gaps.

    P1(0,4), P2(1,3), P3(2,2)
    P1 [0-4], P2 [4-7], P3 [7-9]
    Waiting:  P1=0, P2=3, P3=5
    Turnaround: P1=4, P2=6, P3=7
    """
    procs = [
        Process(1, 0, 4),
        Process(2, 1, 3),
        Process(3, 2, 2),
    ]
    result, timeline = fcfs_schedule(procs)
    by_pid = _by_pid(result)

    assert timeline == [(1, 0, 4), (2, 4, 7), (3, 7, 9)]
    assert by_pid[1].waiting_time == 0
    assert by_pid[1].turnaround_time == 4
    assert by_pid[2].waiting_time == 3
    assert by_pid[2].turnaround_time == 6
    assert by_pid[3].waiting_time == 5
    assert by_pid[3].turnaround_time == 7


def test_fcfs_with_idle_gap():
    """CPU idles when the next process has not arrived yet.

    P1(0,2), P2(5,3)
    P1 [0-2], IDLE [2-5], P2 [5-8]
    Waiting: P1=0, P2=0
    Turnaround: P1=2, P2=3
    """
    procs = [
        Process(1, 0, 2),
        Process(2, 5, 3),
    ]
    result, timeline = fcfs_schedule(procs)
    by_pid = _by_pid(result)

    assert timeline == [(1, 0, 2), ("IDLE", 2, 5), (2, 5, 8)]
    assert by_pid[1].waiting_time == 0
    assert by_pid[1].turnaround_time == 2
    assert by_pid[1].response_time == 0
    assert by_pid[2].waiting_time == 0
    assert by_pid[2].turnaround_time == 3
    assert by_pid[2].response_time == 0
