"""Process / PCB data model for the CPU scheduling simulator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Process:
    """Process Control Block (PCB) used by all scheduling algorithms.

    Attributes:
        pid: Unique process identifier (non-negative integer).
        arrival_time: Time at which the process enters the ready queue (>= 0).
        burst_time: CPU burst length in time units (> 0).
        priority: Optional priority value (used by priority scheduling).
            Lower numbers mean higher priority by default in this project.
        remaining_time: Remaining burst for preemptive algorithms.
        start_time: First time the process was granted the CPU.
        completion_time: Time when the process finished.
        waiting_time: Total time spent waiting in the ready queue.
        turnaround_time: completion_time - arrival_time.
        response_time: start_time - arrival_time (first response latency).
    """

    pid: int
    arrival_time: int
    burst_time: int
    priority: Optional[int] = None
    remaining_time: Optional[int] = None
    start_time: Optional[int] = None
    completion_time: Optional[int] = None
    waiting_time: Optional[int] = None
    turnaround_time: Optional[int] = None
    response_time: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate fields and initialize remaining_time from burst_time."""
        if not isinstance(self.pid, int) or isinstance(self.pid, bool):
            raise ValueError(f"pid must be an integer, got {type(self.pid).__name__}")
        if self.pid < 0:
            raise ValueError(f"pid must be non-negative, got {self.pid}")

        if not isinstance(self.arrival_time, int) or isinstance(self.arrival_time, bool):
            raise ValueError(
                f"arrival_time must be an integer, got {type(self.arrival_time).__name__}"
            )
        if self.arrival_time < 0:
            raise ValueError(
                f"arrival_time must be non-negative, got {self.arrival_time}"
            )

        if not isinstance(self.burst_time, int) or isinstance(self.burst_time, bool):
            raise ValueError(
                f"burst_time must be an integer, got {type(self.burst_time).__name__}"
            )
        if self.burst_time <= 0:
            raise ValueError(f"burst_time must be positive, got {self.burst_time}")

        if self.priority is not None:
            if not isinstance(self.priority, int) or isinstance(self.priority, bool):
                raise ValueError(
                    f"priority must be an integer or None, got {type(self.priority).__name__}"
                )

        if self.remaining_time is None:
            self.remaining_time = self.burst_time
        elif not isinstance(self.remaining_time, int) or isinstance(
            self.remaining_time, bool
        ):
            raise ValueError(
                f"remaining_time must be an integer, got {type(self.remaining_time).__name__}"
            )
        elif self.remaining_time < 0:
            raise ValueError(
                f"remaining_time must be non-negative, got {self.remaining_time}"
            )

        for name in (
            "start_time",
            "completion_time",
            "waiting_time",
            "turnaround_time",
            "response_time",
        ):
            value = getattr(self, name)
            if value is not None and (
                not isinstance(value, int) or isinstance(value, bool)
            ):
                raise ValueError(
                    f"{name} must be an integer or None, got {type(value).__name__}"
                )
            if value is not None and name in ("start_time", "completion_time") and value < 0:
                raise ValueError(f"{name} must be non-negative, got {value}")

    def reset_metrics(self) -> None:
        """Clear scheduling results and restore remaining_time to burst_time."""
        self.remaining_time = self.burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None
        self.response_time = None

    def copy(self) -> Process:
        """Return a fresh Process copy with metrics cleared for a new simulation."""
        return Process(
            pid=self.pid,
            arrival_time=self.arrival_time,
            burst_time=self.burst_time,
            priority=self.priority,
        )

    def finalize_times(self) -> None:
        """Derive waiting, turnaround, and response times from start/completion."""
        if self.completion_time is None:
            raise ValueError(
                f"Process {self.pid}: completion_time is required to finalize metrics"
            )
        if self.start_time is None:
            raise ValueError(
                f"Process {self.pid}: start_time is required to finalize metrics"
            )

        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time
        self.response_time = self.start_time - self.arrival_time

        if self.turnaround_time < 0:
            raise ValueError(
                f"Process {self.pid}: turnaround_time cannot be negative "
                f"({self.turnaround_time})"
            )
        if self.waiting_time < 0:
            raise ValueError(
                f"Process {self.pid}: waiting_time cannot be negative "
                f"({self.waiting_time})"
            )
        if self.response_time < 0:
            raise ValueError(
                f"Process {self.pid}: response_time cannot be negative "
                f"({self.response_time})"
            )

    def __repr__(self) -> str:
        return (
            f"Process(pid={self.pid}, arrival={self.arrival_time}, "
            f"burst={self.burst_time}, priority={self.priority}, "
            f"remaining={self.remaining_time}, start={self.start_time}, "
            f"completion={self.completion_time}, waiting={self.waiting_time}, "
            f"turnaround={self.turnaround_time}, response={self.response_time})"
        )


# Timeline segment: (pid or "IDLE", start_time, end_time)
TimelineEntry = tuple[int | str, int, int]
ScheduleResult = tuple[list[Process], list[TimelineEntry]]
