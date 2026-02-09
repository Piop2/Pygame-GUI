from __future__ import annotations


class Snapshot[T]:
    def __init__(self, state: T) -> None:
        self._state = state
        return

    @property
    def state(self) -> T:
        return self._state
