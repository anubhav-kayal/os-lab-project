"""Process input form for the CPU scheduling simulator GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

from models import Process


ALGORITHM_OPTIONS = (
    "FCFS",
    "SJF (non-preemptive)",
    "SJF (preemptive / SRTF)",
    "Priority (non-preemptive)",
    "Priority (preemptive)",
    "Round Robin",
)

PRIORITY_ALGORITHMS = {
    "Priority (non-preemptive)",
    "Priority (preemptive)",
}


class InputForm(ttk.Frame):
    """Tkinter frame for entering processes and choosing a scheduling algorithm.

    Args:
        master: Parent widget.
        on_run: Callback invoked with ``(processes, algorithm_name, quantum)``
            when the user clicks Run Simulation.
    """

    def __init__(
        self,
        master: tk.Misc,
        on_run: Callable[[list[Process], str, Optional[int]], None],
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._on_run = on_run
        self._next_pid = 1
        self._rows: list[dict] = []

        self.columnconfigure(0, weight=1)

        title = ttk.Label(self, text="Process Input", font=("Helvetica", 14, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))

        controls = ttk.Frame(self)
        controls.grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Algorithm:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.algorithm_var = tk.StringVar(value=ALGORITHM_OPTIONS[0])
        self.algorithm_combo = ttk.Combobox(
            controls,
            textvariable=self.algorithm_var,
            values=ALGORITHM_OPTIONS,
            state="readonly",
            width=28,
        )
        self.algorithm_combo.grid(row=0, column=1, sticky="w")
        self.algorithm_combo.bind("<<ComboboxSelected>>", self._on_algorithm_changed)

        ttk.Label(controls, text="Time quantum:").grid(
            row=0, column=2, sticky="w", padx=(16, 6)
        )
        self.quantum_var = tk.StringVar(value="2")
        self.quantum_entry = ttk.Entry(
            controls, textvariable=self.quantum_var, width=8, state="disabled"
        )
        self.quantum_entry.grid(row=0, column=3, sticky="w")

        table_frame = ttk.LabelFrame(self, text="Processes")
        table_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=4)
        table_frame.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        headers = ("PID", "Arrival", "Burst", "Priority")
        header_row = ttk.Frame(table_frame)
        header_row.grid(row=0, column=0, sticky="ew", padx=4, pady=2)
        for col, text in enumerate(headers):
            ttk.Label(header_row, text=text, width=10).grid(row=0, column=col, padx=2)

        self._rows_container = ttk.Frame(table_frame)
        self._rows_container.grid(row=1, column=0, sticky="ew", padx=4, pady=2)

        button_row = ttk.Frame(self)
        button_row.grid(row=3, column=0, sticky="ew", padx=8, pady=8)

        self.add_btn = ttk.Button(button_row, text="Add Process", command=self.add_process_row)
        self.add_btn.pack(side="left", padx=(0, 6))

        self.remove_btn = ttk.Button(
            button_row, text="Remove Selected", command=self.remove_selected_row
        )
        self.remove_btn.pack(side="left", padx=(0, 6))

        self.run_btn = ttk.Button(
            button_row, text="Run Simulation", command=self._handle_run
        )
        self.run_btn.pack(side="right")

        self.status_var = tk.StringVar(value="Add at least one process to run a simulation.")
        ttk.Label(self, textvariable=self.status_var, foreground="#555").grid(
            row=4, column=0, sticky="w", padx=8, pady=(0, 8)
        )

        self._selected_index: Optional[int] = None
        self.add_process_row(arrival="0", burst="5", priority="1")
        self.add_process_row(arrival="1", burst="3", priority="2")
        self.add_process_row(arrival="2", burst="4", priority="1")
        self._on_algorithm_changed()
        self._refresh_run_state()

    def add_process_row(
        self,
        arrival: str = "0",
        burst: str = "1",
        priority: str = "1",
    ) -> None:
        """Append a new editable process row with an auto-generated PID."""
        row_frame = ttk.Frame(self._rows_container)
        row_index = len(self._rows)
        row_frame.grid(row=row_index, column=0, sticky="ew", pady=1)

        pid_var = tk.StringVar(value=str(self._next_pid))
        arrival_var = tk.StringVar(value=arrival)
        burst_var = tk.StringVar(value=burst)
        priority_var = tk.StringVar(value=priority)
        self._next_pid += 1

        pid_entry = ttk.Entry(row_frame, textvariable=pid_var, width=10, state="readonly")
        arrival_entry = ttk.Entry(row_frame, textvariable=arrival_var, width=10)
        burst_entry = ttk.Entry(row_frame, textvariable=burst_var, width=10)
        priority_entry = ttk.Entry(row_frame, textvariable=priority_var, width=10)

        pid_entry.grid(row=0, column=0, padx=2)
        arrival_entry.grid(row=0, column=1, padx=2)
        burst_entry.grid(row=0, column=2, padx=2)
        priority_entry.grid(row=0, column=3, padx=2)

        def select(_event: tk.Event | None = None, idx: int = row_index) -> None:
            self._selected_index = idx
            self._highlight_selection()

        for widget in (row_frame, pid_entry, arrival_entry, burst_entry, priority_entry):
            widget.bind("<Button-1>", select)

        self._rows.append(
            {
                "frame": row_frame,
                "pid": pid_var,
                "arrival": arrival_var,
                "burst": burst_var,
                "priority": priority_var,
                "priority_entry": priority_entry,
            }
        )
        self._apply_priority_state()
        self._refresh_run_state()
        self._reindex_rows()

    def remove_selected_row(self) -> None:
        """Remove the currently selected process row, if any."""
        if self._selected_index is None or not self._rows:
            messagebox.showinfo("Remove Process", "Select a process row first.")
            return
        idx = self._selected_index
        row = self._rows.pop(idx)
        row["frame"].destroy()
        self._selected_index = None
        self._reindex_rows()
        self._refresh_run_state()

    def get_processes(self) -> list[Process]:
        """Validate and return Process objects from the form rows.

        Raises:
            ValueError: On empty fields, non-integers, or negative values.
        """
        if not self._rows:
            raise ValueError("Add at least one process before running the simulation.")

        processes: list[Process] = []
        seen_pids: set[int] = set()
        needs_priority = self.algorithm_var.get() in PRIORITY_ALGORITHMS

        for i, row in enumerate(self._rows, start=1):
            try:
                pid = int(row["pid"].get().strip())
                arrival = int(row["arrival"].get().strip())
                burst = int(row["burst"].get().strip())
            except ValueError as exc:
                raise ValueError(
                    f"Row {i}: PID, arrival, and burst must be integers."
                ) from exc

            if arrival < 0:
                raise ValueError(f"Row {i}: arrival time cannot be negative.")
            if burst <= 0:
                raise ValueError(f"Row {i}: burst time must be a positive integer.")
            if pid in seen_pids:
                raise ValueError(f"Row {i}: duplicate PID {pid}.")
            seen_pids.add(pid)

            priority: Optional[int] = None
            if needs_priority:
                raw = row["priority"].get().strip()
                if raw == "":
                    raise ValueError(f"Row {i}: priority is required for Priority algorithms.")
                try:
                    priority = int(raw)
                except ValueError as exc:
                    raise ValueError(f"Row {i}: priority must be an integer.") from exc

            processes.append(
                Process(
                    pid=pid,
                    arrival_time=arrival,
                    burst_time=burst,
                    priority=priority,
                )
            )
        return processes

    def get_quantum(self) -> Optional[int]:
        """Return the time quantum when Round Robin is selected."""
        if self.algorithm_var.get() != "Round Robin":
            return None
        raw = self.quantum_var.get().strip()
        if raw == "":
            raise ValueError("Time quantum is required for Round Robin.")
        try:
            quantum = int(raw)
        except ValueError as exc:
            raise ValueError("Time quantum must be a positive integer.") from exc
        if quantum <= 0:
            raise ValueError("Time quantum must be a positive integer.")
        return quantum

    def _handle_run(self) -> None:
        try:
            processes = self.get_processes()
            quantum = self.get_quantum()
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return
        self._on_run(processes, self.algorithm_var.get(), quantum)

    def _on_algorithm_changed(self, _event: tk.Event | None = None) -> None:
        is_rr = self.algorithm_var.get() == "Round Robin"
        self.quantum_entry.configure(state="normal" if is_rr else "disabled")
        self._apply_priority_state()

    def _apply_priority_state(self) -> None:
        enabled = self.algorithm_var.get() in PRIORITY_ALGORITHMS
        state = "normal" if enabled else "disabled"
        for row in self._rows:
            row["priority_entry"].configure(state=state)

    def _reindex_rows(self) -> None:
        for idx, row in enumerate(self._rows):
            row["frame"].grid(row=idx, column=0, sticky="ew", pady=1)

            def select(_event: tk.Event | None = None, i: int = idx) -> None:
                self._selected_index = i
                self._highlight_selection()

            for child in row["frame"].winfo_children():
                child.bind("<Button-1>", select)
            row["frame"].bind("<Button-1>", select)

    def _highlight_selection(self) -> None:
        for idx, row in enumerate(self._rows):
            style = "Selected.TFrame" if idx == self._selected_index else "TFrame"
            # Fallback visual cue via relief on entries
            relief = "solid" if idx == self._selected_index else "flat"
            for child in row["frame"].winfo_children():
                if isinstance(child, ttk.Entry):
                    try:
                        child.configure(style=style)
                    except tk.TclError:
                        pass

    def _refresh_run_state(self) -> None:
        has_rows = bool(self._rows)
        self.run_btn.configure(state="normal" if has_rows else "disabled")
        if not has_rows:
            self.status_var.set("Add at least one process to run a simulation.")
        else:
            self.status_var.set(f"{len(self._rows)} process(es) ready.")
