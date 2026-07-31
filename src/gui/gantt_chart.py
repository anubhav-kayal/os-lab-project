"""Gantt chart visualization using matplotlib embedded in Tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Iterable

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Patch


# Stable color palette keyed by process id modulo palette length.
_PID_COLORS = [
    "#4C78A8",
    "#F58518",
    "#54A24B",
    "#E45756",
    "#72B7B2",
    "#EECA3B",
    "#B279A2",
    "#FF9DA6",
    "#9D755D",
    "#BAB0AC",
]
_IDLE_COLOR = "#B0B0B0"


def color_for_pid(pid: int | str) -> str:
    """Return a consistent color for a process id (or grey for IDLE)."""
    if pid == "IDLE":
        return _IDLE_COLOR
    return _PID_COLORS[int(pid) % len(_PID_COLORS)]


class GanttChart(ttk.Frame):
    """Horizontal one-row Gantt chart for a scheduling timeline.

    Blocks are drawn proportionally to duration and adjacent segments touch
    with no artificial gaps (IDLE is only shown when truly idle).
    """

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._figure = Figure(figsize=(8, 2.2), dpi=100)
        self._ax = self._figure.add_subplot(111)
        self._canvas = FigureCanvasTkAgg(self._figure, master=self)
        self._canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.clear()

    def clear(self) -> None:
        """Reset the chart to an empty placeholder state."""
        self._ax.clear()
        self._ax.set_title("Gantt Chart")
        self._ax.set_xlabel("Time")
        self._ax.set_yticks([])
        self._ax.set_xlim(0, 1)
        self._ax.text(0.5, 0.5, "Run a simulation to render the timeline", ha="center", va="center")
        self._figure.tight_layout()
        self._canvas.draw_idle()

    def render(self, timeline: list[tuple], title: str = "Gantt Chart") -> None:
        """Draw timeline segments as a single-row horizontal bar chart.

        Args:
            timeline: List of ``(pid|"IDLE", start, end)`` tuples.
            title: Chart title (usually includes the algorithm name).
        """
        self._ax.clear()
        self._ax.set_title(title)
        self._ax.set_xlabel("Time")
        self._ax.set_yticks([0])
        self._ax.set_yticklabels(["CPU"])

        if not timeline:
            self._ax.text(0.5, 0.5, "Empty timeline", ha="center", va="center")
            self._canvas.draw_idle()
            return

        t_min = timeline[0][1]
        t_max = timeline[-1][2]
        seen_pids: list[int | str] = []

        for pid, start, end in timeline:
            width = end - start
            if width <= 0:
                continue
            color = color_for_pid(pid)
            self._ax.barh(
                0,
                width,
                left=start,
                height=0.6,
                align="center",
                color=color,
                edgecolor="black",
                linewidth=0.6,
            )
            label = "IDLE" if pid == "IDLE" else f"P{pid}"
            if width > 0:
                self._ax.text(
                    start + width / 2,
                    0,
                    label,
                    ha="center",
                    va="center",
                    color="white" if pid != "IDLE" else "#333",
                    fontsize=9,
                    fontweight="bold",
                )
            if pid not in seen_pids:
                seen_pids.append(pid)

        self._ax.set_xlim(t_min, max(t_max, t_min + 1))
        self._ax.set_ylim(-0.8, 0.8)
        self._add_legend(seen_pids)
        self._figure.tight_layout()
        self._canvas.draw_idle()

    def _add_legend(self, pids: Iterable[int | str]) -> None:
        handles = []
        for pid in pids:
            label = "IDLE" if pid == "IDLE" else f"P{pid}"
            handles.append(Patch(facecolor=color_for_pid(pid), edgecolor="black", label=label))
        if handles:
            self._ax.legend(
                handles=handles,
                loc="upper center",
                bbox_to_anchor=(0.5, -0.22),
                ncol=min(len(handles), 6),
                frameon=False,
                fontsize=8,
            )
