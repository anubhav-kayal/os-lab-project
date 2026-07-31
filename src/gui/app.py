"""Main Tkinter application window for the CPU scheduling simulator."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from models import Process
from scheduler import run_algorithm
from metrics import summarize
from gui.input_form import InputForm


class SchedulingApp(tk.Tk):
    """Root application window (Phase 7: console-output wiring)."""

    def __init__(self) -> None:
        super().__init__()
        self.title("CPU Scheduling Simulator")
        self.geometry("780x420")
        self.minsize(700, 360)

        container = ttk.Frame(self, padding=8)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.input_form = InputForm(container, on_run=self.handle_run)
        self.input_form.grid(row=0, column=0, sticky="nsew")

        hint = ttk.Label(
            container,
            text="Phase 7: Run Simulation prints results to the console. "
            "Gantt chart arrives in Phase 8.",
            foreground="#666",
        )
        hint.grid(row=1, column=0, sticky="w", pady=(8, 0))

    def handle_run(
        self,
        processes: list[Process],
        algorithm_name: str,
        time_quantum: Optional[int],
    ) -> None:
        """Execute the selected algorithm and print a concise console report."""
        result, timeline = run_algorithm(algorithm_name, processes, time_quantum)
        stats = summarize(result, timeline)

        print("=" * 60)
        print(f"Algorithm: {algorithm_name}")
        if time_quantum is not None:
            print(f"Time quantum: {time_quantum}")
        print("-" * 60)
        print(
            f"{'PID':>4} {'AT':>4} {'BT':>4} {'ST':>4} {'CT':>4} "
            f"{'WT':>4} {'TAT':>4} {'RT':>4}"
        )
        for p in sorted(result, key=lambda x: x.pid):
            print(
                f"{p.pid:>4} {p.arrival_time:>4} {p.burst_time:>4} "
                f"{p.start_time:>4} {p.completion_time:>4} "
                f"{p.waiting_time:>4} {p.turnaround_time:>4} {p.response_time:>4}"
            )
        print("-" * 60)
        print(f"Timeline: {timeline}")
        print(
            f"Avg WT={stats['avg_waiting_time']:.2f}  "
            f"Avg TAT={stats['avg_turnaround_time']:.2f}  "
            f"Avg RT={stats['avg_response_time']:.2f}"
        )
        print(
            f"CPU util={stats['cpu_utilization']:.1f}%  "
            f"Throughput={stats['throughput']:.3f}"
        )
        print("=" * 60)


def run_app() -> None:
    """Create and start the Tkinter main loop."""
    app = SchedulingApp()
    app.mainloop()
