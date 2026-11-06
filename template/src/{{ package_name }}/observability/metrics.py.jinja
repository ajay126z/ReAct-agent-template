"""Per-run counters and timings."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class RunMetrics:
    """Mutable counters collected while a run is in progress."""

    llm_calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    tool_calls: int = 0
    tool_errors: int = 0
    parse_retries: int = 0
    steps: int = 0
    llm_duration_ms: float = 0.0
    tool_duration_ms: float = 0.0
    started_perf: float = field(default_factory=time.perf_counter, repr=False)
    wall_time_ms: float = 0.0

    def record_llm(
        self, *, prompt_tokens: int | None, completion_tokens: int | None, duration_ms: float
    ) -> None:
        self.llm_calls += 1
        self.prompt_tokens += prompt_tokens or 0
        self.completion_tokens += completion_tokens or 0
        self.llm_duration_ms += duration_ms

    def record_tool(self, *, duration_ms: float, is_error: bool) -> None:
        self.tool_calls += 1
        self.tool_duration_ms += duration_ms
        if is_error:
            self.tool_errors += 1

    def finish(self) -> None:
        self.wall_time_ms = (time.perf_counter() - self.started_perf) * 1000.0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def as_dict(self) -> dict[str, int | float]:
        self.finish()
        return {
            "llm_calls": self.llm_calls,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "tool_calls": self.tool_calls,
            "tool_errors": self.tool_errors,
            "parse_retries": self.parse_retries,
            "steps": self.steps,
            "llm_duration_ms": round(self.llm_duration_ms, 2),
            "tool_duration_ms": round(self.tool_duration_ms, 2),
            "wall_time_ms": round(self.wall_time_ms, 2),
        }
