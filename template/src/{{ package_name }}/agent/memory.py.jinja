"""Bounded conversation memory and JSONL session persistence."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from ..observability.logging import get_logger

log = get_logger("agent.memory")

_SESSION_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


@dataclass(frozen=True, slots=True)
class ConversationTurn:
    """One completed question/answer pair."""

    question: str
    answer: str
    timestamp: str
    model: str = ""

    @classmethod
    def create(cls, question: str, answer: str, *, model: str = "") -> ConversationTurn:
        return cls(
            question=question,
            answer=answer,
            timestamp=datetime.now(UTC).isoformat(),
            model=model,
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "timestamp": self.timestamp,
            "question": self.question,
            "answer": self.answer,
            "model": self.model,
        }

    @classmethod
    def from_dict(cls, data: object) -> ConversationTurn:
        if not isinstance(data, dict):
            raise ValueError("session entry must be a JSON object")
        question = data.get("question")
        answer = data.get("answer")
        if not isinstance(question, str) or not isinstance(answer, str):
            raise ValueError("session entry needs string question and answer fields")
        timestamp = data.get("timestamp", "")
        model = data.get("model", "")
        return cls(
            question=question,
            answer=answer,
            timestamp=timestamp if isinstance(timestamp, str) else "",
            model=model if isinstance(model, str) else "",
        )


@dataclass
class ConversationMemory:
    """Recent Q/A turns bounded by count and total characters."""

    max_turns: int = 6
    max_chars: int = 4000
    turns: list[ConversationTurn] = field(default_factory=list)

    def add(self, turn: ConversationTurn) -> None:
        self.turns.append(turn)
        self._trim()

    def extend(self, turns: Iterable[ConversationTurn]) -> None:
        self.turns.extend(turns)
        self._trim()

    def clear(self) -> None:
        self.turns.clear()

    def _trim(self) -> None:
        if self.max_turns > 0 and len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns :]

        total = sum(len(turn.question) + len(turn.answer) for turn in self.turns)
        while self.turns and total > self.max_chars:
            removed = self.turns.pop(0)
            total -= len(removed.question) + len(removed.answer)

    def __len__(self) -> int:
        return len(self.turns)


@dataclass(frozen=True, slots=True)
class SessionInfo:
    name: str
    path: Path
    turns: int
    updated_at: datetime


class SessionStore:
    """Read and write sessions as append-only JSONL files."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.archive_dir = root / "archive"

    @staticmethod
    def validate_name(name: str) -> str:
        if not _SESSION_NAME.fullmatch(name):
            raise ValueError(
                "Session names must start with a letter or digit and contain only "
                "letters, digits, dots, dashes, or underscores (max 64 characters)."
            )
        return name

    def path(self, name: str) -> Path:
        return self.root / f"{self.validate_name(name)}.jsonl"

    def exists(self, name: str) -> bool:
        return self.path(name).is_file()

    def _iter_turns(self, path: Path, name: str) -> Iterator[ConversationTurn]:
        if not path.exists():
            return
        try:
            with path.open(encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield ConversationTurn.from_dict(json.loads(line))
                    except (json.JSONDecodeError, ValueError, TypeError) as exc:
                        log.warning(
                            "skipping corrupt session line session=%s line=%d error=%s",
                            name,
                            line_number,
                            exc,
                        )
        except OSError as exc:
            raise ValueError(f"Could not read session {name!r}: {exc}") from exc

    def load(self, name: str, *, max_turns: int, max_chars: int) -> ConversationMemory:
        memory = ConversationMemory(max_turns=max_turns, max_chars=max_chars)
        memory.extend(self._iter_turns(self.path(name), name))
        return memory

    def append(self, name: str, turn: ConversationTurn) -> None:
        path = self.path(name)
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(turn.to_dict(), ensure_ascii=False) + "\n")
        except OSError as exc:
            raise ValueError(f"Could not write session {name!r}: {exc}") from exc

    def reset(self, name: str) -> Path | None:
        path = self.path(name)
        if not path.exists():
            return None

        try:
            self.archive_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
            archived = self.archive_dir / f"{name}-{stamp}.jsonl"
            suffix = 1
            while archived.exists():
                archived = self.archive_dir / f"{name}-{stamp}-{suffix}.jsonl"
                suffix += 1
            path.replace(archived)
        except OSError as exc:
            raise ValueError(f"Could not archive session {name!r}: {exc}") from exc
        return archived

    def delete(self, name: str) -> bool:
        path = self.path(name)
        if not path.exists():
            return False
        try:
            path.unlink()
        except OSError as exc:
            raise ValueError(f"Could not delete session {name!r}: {exc}") from exc
        return True

    def latest(self) -> str | None:
        sessions = self.list_sessions()
        return sessions[0].name if sessions else None

    def list_sessions(self) -> list[SessionInfo]:
        if not self.root.is_dir():
            return []

        sessions: list[SessionInfo] = []
        for path in self.root.glob("*.jsonl"):
            if not path.is_file():
                continue
            try:
                name = self.validate_name(path.stem)
                stat = path.stat()
                turns = sum(1 for _ in self._iter_turns(path, name))
            except (OSError, ValueError) as exc:
                log.warning("skipping unreadable session path=%s error=%s", path, exc)
                continue
            sessions.append(
                SessionInfo(
                    name=name,
                    path=path,
                    turns=turns,
                    updated_at=datetime.fromtimestamp(stat.st_mtime, tz=UTC),
                )
            )

        sessions.sort(key=lambda session: session.updated_at, reverse=True)
        return sessions
