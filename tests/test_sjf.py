"""Unit tests for SJF (non-preemptive) and SRTF (preemptive SJF)."""

from __future__ import annotations

from models import Process
from algorithms.sjf import sjf_non_preemptive, sjf_preemptive


def _by_pid(processes: list[Process]) -> dict[int, Process]:
    return {p.pid: p for p in processes}


def test_sjf_non_preemptive_staggered():
    """Non-preemptive SJF with staggered arrivals.

    P1(0,7), P2(2,4), P3(4,1), P4(5,4)
    t=0: only P1 → runs [0-7] (non-preemptive, ignores shorter later arrivals)
    At t=7 ready: P2(4), P3(1), P4(4) → pick P3 [7-8], then P2 [8-12]
    (pid 2 before 4 on equal burst), then P4 [12-16]

    Waiting: P1=0, P2=6, P3=3, P4=7
    Turnaround: P1=7, P2=10, P3=4, P4=11
    """
    procs = [
        Process(1, 0, 7),
        Process(2, 2, 4),
        Process(3, 4, 1),
        Process(4, 5, 4),
    ]
    result, timeline = sjf_non_preemptive(procs)
    by_pid = _by_pid(result)

    assert timeline == [
        (1, 0, 7),
        (3, 7, 8),
        (2, 8, 12),
        (4, 12, 16),
    ]
    assert by_pid[1].waiting_time == 0
    assert by_pid[1].turnaround_time == 7
    assert by_pid[2].waiting_time == 6
    assert by_pid[2].turnaround_time == 10
    assert by_pid[3].waiting_time == 3
    assert by_pid[3].turnaround_time == 4
    assert by_pid[4].waiting_time == 7
    assert by_pid[4].turnaround_time == 11


def test_sjf_preemptive_mid_execution():
    """SRTF: shorter job arrives mid-execution and preempts.

    P1(0,8), P2(1,4), P3(2,9), P4(3,5)
    t=0: P1 runs
    t=1: P2 arrives (rem 4) < P1 rem 7 → preempt, P2 runs
    t=2: P3 arrives (9); P2 still shortest
    t=3: P4 arrives (5); P2 still shortest
    t=5: P2 done. Ready rem: P1=7, P3=9, P4=5 → P4
    t=10: P4 done. Ready: P1=7, P3=9 → P1
    t=17: P1 done → P3 [17-26]

    Timeline:
      P1 [0-1], P2 [1-5], P4 [5-10], P1 [10-17], P3 [17-26]

    Waiting: P1=(1-0)+(10-1)- wait calc via finalize
      TAT P1=17-0=17, WT=17-8=9
      TAT P2=5-1=4, WT=4-4=0
      TAT P3=26-2=24, WT=24-9=15
      TAT P4=10-3=7, WT=7-5=2
    """
    procs = [
        Process(1, 0, 8),
        Process(2, 1, 4),
        Process(3, 2, 9),
        Process(4, 3, 5),
    ]
    result, timeline = sjf_preemptive(procs)
    by_pid = _by_pid(result)

    assert timeline == [
        (1, 0, 1),
        (2, 1, 5),
        (4, 5, 10),
        (1, 10, 17),
        (3, 17, 26),
    ]
    assert by_pid[1].waiting_time == 9
    assert by_pid[1].turnaround_time == 17
    assert by_pid[1].response_time == 0
    assert by_pid[2].waiting_time == 0
    assert by_pid[2].turnaround_time == 4
    assert by_pid[2].response_time == 0
    assert by_pid[3].waiting_time == 15
    assert by_pid[3].turnaround_time == 24
    assert by_pid[4].waiting_time == 2
    assert by_pid[4].turnaround_time == 7


def test_sjf_tie_break_lower_pid():
    """Equal burst times: lower pid wins."""
    procs = [
        Process(2, 0, 3),
        Process(1, 0, 3),
    ]
    result, timeline = sjf_non_preemptive(procs)
    assert [p.pid for p in result] == [1, 2]
    assert timeline == [(1, 0, 3), (2, 3, 6)]
