"""Unit tests for Round Robin scheduling."""

from __future__ import annotations

from models import Process
from algorithms.round_robin import round_robin_schedule


def _by_pid(processes: list[Process]) -> dict[int, Process]:
    return {p.pid: p for p in processes}


def test_round_robin_quantum_1():
    """Quantum=1 rotates every time unit.

    P1(0,3), P2(0,2), P3(0,1) — all at t=0, ready order by pid: 1,2,3
    Timeline:
      P1[0-1], P2[1-2], P3[2-3], P1[3-4], P2[4-5], P1[5-6]
    Completion: P3=3, P2=5, P1=6
    Waiting: P1=3, P2=3, P3=2
    Turnaround: P1=6, P2=5, P3=3
    """
    procs = [
        Process(1, 0, 3),
        Process(2, 0, 2),
        Process(3, 0, 1),
    ]
    result, timeline = round_robin_schedule(procs, time_quantum=1)
    by_pid = _by_pid(result)

    assert timeline == [
        (1, 0, 1),
        (2, 1, 2),
        (3, 2, 3),
        (1, 3, 4),
        (2, 4, 5),
        (1, 5, 6),
    ]
    assert by_pid[1].waiting_time == 3
    assert by_pid[1].turnaround_time == 6
    assert by_pid[1].response_time == 0
    assert by_pid[2].waiting_time == 3
    assert by_pid[2].turnaround_time == 5
    assert by_pid[3].waiting_time == 2
    assert by_pid[3].turnaround_time == 3


def test_round_robin_quantum_4():
    """Quantum=4 with staggered arrivals.

    P1(0,5), P2(1,4), P3(2,2), quantum=4
    t=0: queue [P1]; P1 runs [0-4], remaining=1
      During [0-4]: P2@1 and P3@2 arrive → queue [P2, P3] then P1 re-enters → [P2,P3,P1]
    P2 runs [4-8], done
      queue [P3, P1]
    P3 runs [8-10], done
      queue [P1]
    P1 runs [10-11], done

    Waiting: P1=6, P2=3, P3=6
    Turnaround: P1=11, P2=7, P3=8
    """
    procs = [
        Process(1, 0, 5),
        Process(2, 1, 4),
        Process(3, 2, 2),
    ]
    result, timeline = round_robin_schedule(procs, time_quantum=4)
    by_pid = _by_pid(result)

    assert timeline == [
        (1, 0, 4),
        (2, 4, 8),
        (3, 8, 10),
        (1, 10, 11),
    ]
    assert by_pid[1].waiting_time == 6
    assert by_pid[1].turnaround_time == 11
    assert by_pid[2].waiting_time == 3
    assert by_pid[2].turnaround_time == 7
    assert by_pid[3].waiting_time == 6
    assert by_pid[3].turnaround_time == 8


def test_round_robin_quantum_larger_than_bursts_like_fcfs():
    """When quantum > all bursts, RR behaves like FCFS (no preemption).

    P1(0,3), P2(1,2), P3(4,1), quantum=10
    P1 [0-3], P2 [3-5], IDLE? P3 arrives at 4 while P2 running —
    at t=3 queue has P2 (arrived at 1). P2 [3-5]. P3 arrived at 4 during P2 →
    queued. P3 [5-6].
    Same as FCFS for this set: P1, P2, P3 with no idle.
    Waiting: P1=0, P2=2, P3=1
    """
    procs = [
        Process(1, 0, 3),
        Process(2, 1, 2),
        Process(3, 4, 1),
    ]
    result, timeline = round_robin_schedule(procs, time_quantum=10)
    by_pid = _by_pid(result)

    assert timeline == [(1, 0, 3), (2, 3, 5), (3, 5, 6)]
    assert by_pid[1].waiting_time == 0
    assert by_pid[1].turnaround_time == 3
    assert by_pid[2].waiting_time == 2
    assert by_pid[2].turnaround_time == 4
    assert by_pid[3].waiting_time == 1
    assert by_pid[3].turnaround_time == 2
