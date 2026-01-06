from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Updatable(Protocol):
    def update(self, delta: int) -> None: ...
