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
from gui.comparison_view import ComparisonView, ResultsTable


class SchedulingApp(tk.Tk):
    """Root window: process input, Gantt/results tab, and comparison tab."""

    def __init__(self) -> None:
        super().__init__()
        self.title("CPU Scheduling Simulator")
        self.geometry("960x760")
        self.minsize(860, 680)

        container = ttk.Frame(self, padding=8)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        self.input_form = InputForm(container, on_run=self.handle_run)
        self.input_form.grid(row=0, column=0, sticky="ew")

        self.notebook = ttk.Notebook(container)
        self.notebook.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

        # --- Tab 1: single-algorithm simulation ---
        sim_tab = ttk.Frame(self.notebook, padding=6)
        sim_tab.columnconfigure(0, weight=1)
        sim_tab.rowconfigure(0, weight=1)
        self.notebook.add(sim_tab, text="Simulation")

        self.gantt = GanttChart(sim_tab)
        self.gantt.grid(row=0, column=0, sticky="nsew")

        ttk.Label(sim_tab, text="Per-process results", font=("Helvetica", 11, "bold")).grid(
            row=1, column=0, sticky="w", pady=(8, 2)
        )
        self.results_table = ResultsTable(sim_tab)
        self.results_table.grid(row=2, column=0, sticky="nsew")
        sim_tab.rowconfigure(2, weight=1)

        # --- Tab 2: compare all algorithms ---
        compare_tab = ttk.Frame(self.notebook, padding=6)
        compare_tab.columnconfigure(0, weight=1)
        compare_tab.rowconfigure(0, weight=1)
        self.notebook.add(compare_tab, text="Compare All Algorithms")

        self.comparison = ComparisonView(compare_tab)
        self.comparison.grid(row=0, column=0, sticky="nsew")
        self.comparison.bind_context(self._comparison_context)

        self.status_var = tk.StringVar(
            value="Enter processes and click Run Simulation (or open Compare All Algorithms)."
        )
        ttk.Label(container, textvariable=self.status_var, foreground="#555").grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )

        self._last_processes: list[Process] = []

    def _comparison_context(self) -> tuple[list[Process], Optional[int]]:
        """Provide the current form processes (and RR quantum) to ComparisonView."""
        processes = self.input_form.get_processes()
        # Always read quantum when present so RR participates in comparisons.
        raw = self.input_form.quantum_var.get().strip()
        quantum: Optional[int]
        try:
            quantum = int(raw) if raw else 2
        except ValueError as exc:
            raise ValueError("Time quantum must be a positive integer.") from exc
        if quantum <= 0:
            raise ValueError("Time quantum must be a positive integer.")
        return processes, quantum

    def handle_run(
        self,
        processes: list[Process],
        algorithm_name: str,
        time_quantum: Optional[int],
    ) -> None:
        """Execute the selected algorithm, then refresh Gantt + results table."""
        result, timeline = run_algorithm(algorithm_name, processes, time_quantum)
        stats = summarize(result, timeline)
        title = algorithm_name
        if time_quantum is not None:
            title = f"{algorithm_name} (q={time_quantum})"

        self._last_processes = result
        self.gantt.render(timeline, title=title)
        self.results_table.populate(result)
        self.notebook.select(0)
        self.status_var.set(
            f"{algorithm_name}: Avg WT={stats['avg_waiting_time']:.2f}, "
            f"Avg TAT={stats['avg_turnaround_time']:.2f}, "
            f"CPU={stats['cpu_utilization']:.1f}%"
        )


def run_app() -> None:
    """Create and start the Tkinter main loop."""
    app = SchedulingApp()
    app.mainloop()
