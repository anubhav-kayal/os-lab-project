"""Scheduling performance metrics and cross-algorithm comparison helpers."""

from __future__ import annotations

from models import Process


def _require_completed(processes: list[Process]) -> None:
    if not processes:
        raise ValueError("Cannot compute metrics for an empty process list")
    for p in processes:
        if (
            p.waiting_time is None
            or p.turnaround_time is None
            or p.response_time is None
            or p.completion_time is None
        ):
            raise ValueError(
                f"Process {p.pid} is missing completed scheduling metrics"
            )


def average_waiting_time(processes: list[Process]) -> float:
    """Return the mean waiting time across completed processes."""
    _require_completed(processes)
    return sum(p.waiting_time for p in processes) / len(processes)  # type: ignore[arg-type]


def average_turnaround_time(processes: list[Process]) -> float:
    """Return the mean turnaround time across completed processes."""
    _require_completed(processes)
    return sum(p.turnaround_time for p in processes) / len(processes)  # type: ignore[arg-type]


def average_response_time(processes: list[Process]) -> float:
    """Return the mean response time across completed processes."""
    _require_completed(processes)
    return sum(p.response_time for p in processes) / len(processes)  # type: ignore[arg-type]


def cpu_utilization(processes: list[Process], timeline: list[tuple] | None = None) -> float:
    """Return CPU utilization as a percentage in [0, 100].

    If a Gantt ``timeline`` is provided, utilization is
    ``busy_time / total_span * 100`` where IDLE segments are not busy.
    Otherwise falls back to ``sum(burst) / makespan * 100`` using the latest
    completion time and earliest arrival as the span.
    """
    _require_completed(processes)
    if timeline is not None:
        if not timeline:
            return 0.0
        span_start = timeline[0][1]
        span_end = timeline[-1][2]
        total = span_end - span_start
        if total <= 0:
            return 0.0
        busy = sum(end - start for pid, start, end in timeline if pid != "IDLE")
        return (busy / total) * 100.0

    earliest = min(p.arrival_time for p in processes)
    latest = max(p.completion_time for p in processes)  # type: ignore[type-var]
    total = latest - earliest
    if total <= 0:
        return 100.0 if sum(p.burst_time for p in processes) > 0 else 0.0
    busy = sum(p.burst_time for p in processes)
    return (busy / total) * 100.0


def throughput(processes: list[Process], timeline: list[tuple] | None = None) -> float:
    """Return throughput as processes completed per unit time."""
    _require_completed(processes)
    if timeline is not None:
        if not timeline:
            return 0.0
        span = timeline[-1][2] - timeline[0][1]
    else:
        earliest = min(p.arrival_time for p in processes)
        latest = max(p.completion_time for p in processes)  # type: ignore[type-var]
        span = latest - earliest
    if span <= 0:
        return float(len(processes))
    return len(processes) / span


def summarize(processes: list[Process], timeline: list[tuple] | None = None) -> dict:
    """Build a metrics summary dict for one algorithm run."""
    return {
        "avg_waiting_time": average_waiting_time(processes),
        "avg_turnaround_time": average_turnaround_time(processes),
        "avg_response_time": average_response_time(processes),
        "cpu_utilization": cpu_utilization(processes, timeline),
        "throughput": throughput(processes, timeline),
        "process_count": len(processes),
    }


def compare_algorithms(
    results: dict[str, list[Process]],
    timelines: dict[str, list[tuple]] | None = None,
) -> dict[str, dict]:
    """Compare multiple algorithm runs on (usually) the same process set.

    Args:
        results: Mapping of algorithm name → completed Process list.
        timelines: Optional mapping of algorithm name → Gantt timeline for
            more accurate CPU utilization / throughput.

    Returns:
        Mapping of algorithm name → summarize() metrics dict. Also includes a
        top-level ``\"ranking\"`` key with algorithms ordered by ascending
        average waiting time.
    """
    if not results:
        raise ValueError("results must contain at least one algorithm entry")

    summary: dict[str, dict] = {}
    for name, processes in results.items():
        tl = None if timelines is None else timelines.get(name)
        summary[name] = summarize(processes, tl)

    ranking = sorted(
        results.keys(),
        key=lambda name: summary[name]["avg_waiting_time"],
    )
    return {"by_algorithm": summary, "ranking_by_avg_waiting": ranking}
