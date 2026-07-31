"""Main Tkinter application window for the CPU scheduling simulator."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from models import Process
from scheduler import run_algorithm
from metrics import summarize
from gui.input_form import InputForm
from gui.gantt_chart import GanttChart


class SchedulingApp(tk.Tk):
    """Root application window with process input and Gantt visualization."""

    def __init__(self) -> None:
        super().__init__()
        self.title("CPU Scheduling Simulator")
        self.geometry("900x640")
        self.minsize(800, 560)

        container = ttk.Frame(self, padding=8)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        self.input_form = InputForm(container, on_run=self.handle_run)
        self.input_form.grid(row=0, column=0, sticky="ew")

        self.gantt = GanttChart(container)
        self.gantt.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

        self.status_var = tk.StringVar(
            value="Enter processes and click Run Simulation to draw the Gantt chart."
        )
        ttk.Label(container, textvariable=self.status_var, foreground="#555").grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )

    def handle_run(
        self,
        processes: list[Process],
        algorithm_name: str,
        time_quantum: Optional[int],
    ) -> None:
        """Execute the selected algorithm and render its Gantt chart."""
        result, timeline = run_algorithm(algorithm_name, processes, time_quantum)
        stats = summarize(result, timeline)
        title = algorithm_name
        if time_quantum is not None:
            title = f"{algorithm_name} (q={time_quantum})"
        self.gantt.render(timeline, title=title)
        self.status_var.set(
            f"{algorithm_name}: Avg WT={stats['avg_waiting_time']:.2f}, "
            f"Avg TAT={stats['avg_turnaround_time']:.2f}, "
            f"CPU={stats['cpu_utilization']:.1f}%"
        )


def run_app() -> None:
    """Create and start the Tkinter main loop."""
    app = SchedulingApp()
    app.mainloop()
