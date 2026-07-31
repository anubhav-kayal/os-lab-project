"""Cross-algorithm comparison dashboard and per-process results table."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from models import Process
from metrics import compare_algorithms, summarize
from scheduler import run_algorithm
from gui.input_form import ALGORITHM_OPTIONS


class ResultsTable(ttk.Frame):
    """Treeview showing per-process metrics plus an averages summary row."""

    COLUMNS = (
        "pid",
        "arrival",
        "burst",
        "start",
        "completion",
        "waiting",
        "turnaround",
        "response",
    )
    HEADINGS = {
        "pid": "PID",
        "arrival": "Arrival",
        "burst": "Burst",
        "start": "Start",
        "completion": "Completion",
        "waiting": "Waiting",
        "turnaround": "Turnaround",
        "response": "Response",
    }

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            self,
            columns=self.COLUMNS,
            show="headings",
            height=8,
        )
        for col in self.COLUMNS:
            self.tree.heading(col, text=self.HEADINGS[col])
            self.tree.column(col, width=90, anchor="center")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

    def clear(self) -> None:
        """Remove all rows from the table."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def populate(self, processes: list[Process]) -> None:
        """Fill the table with process metrics and a summary averages row."""
        self.clear()
        if not processes:
            return

        ordered = sorted(processes, key=lambda p: p.pid)
        for p in ordered:
            self.tree.insert(
                "",
                "end",
                values=(
                    p.pid,
                    p.arrival_time,
                    p.burst_time,
                    p.start_time,
                    p.completion_time,
                    p.waiting_time,
                    p.turnaround_time,
                    p.response_time,
                ),
            )

        stats = summarize(ordered)
        self.tree.insert(
            "",
            "end",
            values=(
                "AVG",
                "",
                "",
                "",
                "",
                f"{stats['avg_waiting_time']:.2f}",
                f"{stats['avg_turnaround_time']:.2f}",
                f"{stats['avg_response_time']:.2f}",
            ),
            tags=("summary",),
        )
        self.tree.tag_configure("summary", background="#E8EEF7")


class ComparisonView(ttk.Frame):
    """Run the same process set through all algorithms and chart averages."""

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(
            header,
            text="Compare All Algorithms",
            font=("Helvetica", 12, "bold"),
        ).pack(side="left")
        self.compare_btn = ttk.Button(
            header, text="Run Comparison", command=self._noop_until_bound
        )
        self.compare_btn.pack(side="right")

        self._figure = Figure(figsize=(8, 3.5), dpi=100)
        self._ax = self._figure.add_subplot(111)
        self._canvas = FigureCanvasTkAgg(self._figure, master=self)
        self._canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        self._summary = tk.StringVar(value="Load processes above, then run comparison.")
        ttk.Label(self, textvariable=self._summary, foreground="#555").grid(
            row=2, column=0, sticky="w", pady=(6, 0)
        )

        self._get_context: Callable[[], tuple[list[Process], Optional[int]]] = (
            lambda: ([], None)
        )
        self._clear_chart()

    def bind_context(
        self,
        getter: Callable[[], tuple[list[Process], Optional[int]]],
    ) -> None:
        """Bind a callback that returns ``(processes, round_robin_quantum)``."""
        self._get_context = getter
        self.compare_btn.configure(command=self.run_comparison)

    def _noop_until_bound(self) -> None:
        messagebox.showinfo("Compare", "Comparison is not ready yet.")

    def _clear_chart(self) -> None:
        self._ax.clear()
        self._ax.set_title("Average Waiting / Turnaround by Algorithm")
        self._ax.set_ylabel("Time")
        self._ax.text(0.5, 0.5, "No comparison yet", ha="center", va="center", transform=self._ax.transAxes)
        self._figure.tight_layout()
        self._canvas.draw_idle()

    def run_comparison(self) -> None:
        """Schedule the current process set with every supported algorithm."""
        try:
            processes, quantum = self._get_context()
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return

        if not processes:
            messagebox.showwarning(
                "No Processes",
                "Add at least one process before running the comparison.",
            )
            return

        # Round Robin needs a quantum; fall back to 2 if the form disabled it.
        rr_quantum = quantum if quantum is not None else 2

        results: dict[str, list[Process]] = {}
        timelines: dict[str, list[tuple]] = {}
        errors: list[str] = []

        for name in ALGORITHM_OPTIONS:
            try:
                q = rr_quantum if name == "Round Robin" else None
                # Priority algorithms require priority values on each process.
                if "Priority" in name:
                    if any(p.priority is None for p in processes):
                        # Use a mild default so comparison still works from non-priority runs.
                        procs = [
                            Process(
                                pid=p.pid,
                                arrival_time=p.arrival_time,
                                burst_time=p.burst_time,
                                priority=p.priority if p.priority is not None else p.pid,
                            )
                            for p in processes
                        ]
                    else:
                        procs = processes
                else:
                    procs = processes
                completed, timeline = run_algorithm(name, procs, q)
                results[name] = completed
                timelines[name] = timeline
            except Exception as exc:  # noqa: BLE001 - surface per-algorithm failures
                errors.append(f"{name}: {exc}")

        if not results:
            messagebox.showerror("Comparison Failed", "\n".join(errors) or "No results.")
            return

        comparison = compare_algorithms(results, timelines)
        self._draw_bars(comparison["by_algorithm"])
        best = comparison["ranking_by_avg_waiting"][0]
        self._summary.set(
            f"Lowest avg waiting time: {best} "
            f"({comparison['by_algorithm'][best]['avg_waiting_time']:.2f}). "
            + (f"Skipped: {'; '.join(errors)}" if errors else "")
        )

    def _draw_bars(self, by_algorithm: dict[str, dict]) -> None:
        self._ax.clear()
        names = list(by_algorithm.keys())
        # Short labels for readability
        labels = [self._short_name(n) for n in names]
        waiting = [by_algorithm[n]["avg_waiting_time"] for n in names]
        turnaround = [by_algorithm[n]["avg_turnaround_time"] for n in names]

        x = list(range(len(names)))
        width = 0.35
        self._ax.bar([i - width / 2 for i in x], waiting, width, label="Avg Waiting", color="#4C78A8")
        self._ax.bar(
            [i + width / 2 for i in x],
            turnaround,
            width,
            label="Avg Turnaround",
            color="#F58518",
        )
        self._ax.set_xticks(x)
        self._ax.set_xticklabels(labels, rotation=25, ha="right")
        self._ax.set_ylabel("Time")
        self._ax.set_title("Average Waiting / Turnaround by Algorithm")
        self._ax.legend(frameon=False)
        self._figure.tight_layout()
        self._canvas.draw_idle()

    @staticmethod
    def _short_name(name: str) -> str:
        mapping = {
            "FCFS": "FCFS",
            "SJF (non-preemptive)": "SJF",
            "SJF (preemptive / SRTF)": "SRTF",
            "Priority (non-preemptive)": "Prio NP",
            "Priority (preemptive)": "Prio P",
            "Round Robin": "RR",
        }
        return mapping.get(name, name)
