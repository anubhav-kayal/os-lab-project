"""Unit tests for metrics helpers (hand-computed on a fixed FCFS run)."""

from __future__ import annotations

from models import Process
from algorithms.fcfs import fcfs_schedule
from metrics import (
    average_response_time,
    average_turnaround_time,
    average_waiting_time,
    compare_algorithms,
    cpu_utilization,
    summarize,
    throughput,
)


def _sample_fcfs():
    """Fixed set used across metric assertions.

    P1(0,5), P2(1,3), P3(2,1) under FCFS:
      P1 [0-5], P2 [5-8], P3 [8-9]
    Waiting: 0, 4, 6  → avg = 10/3 ≈ 3.333...
    Turnaround: 5, 7, 7 → avg = 19/3 ≈ 6.333...
    Response: 0, 4, 6 → avg = 10/3
    Busy=9, span=9 → util=100%, throughput=3/9=1/3
    """
    procs = [
        Process(1, 0, 5),
        Process(2, 1, 3),
        Process(3, 2, 1),
    ]
    return fcfs_schedule(procs)


def test_averages_match_hand_calculation():
    result, timeline = _sample_fcfs()
    assert average_waiting_time(result) == 10 / 3
    assert average_turnaround_time(result) == 19 / 3
    assert average_response_time(result) == 10 / 3
    assert cpu_utilization(result, timeline) == 100.0
    assert throughput(result, timeline) == 3 / 9


def test_cpu_utilization_with_idle():
    """P1(0,2), P2(5,3): busy=5, span=8 → util=62.5%."""
    procs = [Process(1, 0, 2), Process(2, 5, 3)]
    result, timeline = fcfs_schedule(procs)
    assert cpu_utilization(result, timeline) == (5 / 8) * 100
    assert throughput(result, timeline) == 2 / 8


def test_summarize_and_compare_algorithms():
    result, timeline = _sample_fcfs()
    summary = summarize(result, timeline)
    assert summary["avg_waiting_time"] == 10 / 3
    assert summary["process_count"] == 3

    # Compare a single algorithm entry (structure check)
    comparison = compare_algorithms(
        {"FCFS": result},
        {"FCFS": timeline},
    )
    assert comparison["ranking_by_avg_waiting"] == ["FCFS"]
    assert comparison["by_algorithm"]["FCFS"]["avg_turnaround_time"] == 19 / 3


def test_compare_ranks_by_waiting_time():
    """Artificial completed processes to verify ranking only."""
    low_wait = [
        Process(1, 0, 1),
    ]
    low_wait[0].start_time = 0
    low_wait[0].completion_time = 1
    low_wait[0].finalize_times()

    high_wait = [
        Process(1, 0, 1),
    ]
    high_wait[0].start_time = 5
    high_wait[0].completion_time = 6
    high_wait[0].finalize_times()

    comparison = compare_algorithms({"A": high_wait, "B": low_wait})
    assert comparison["ranking_by_avg_waiting"] == ["B", "A"]
