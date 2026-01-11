from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Valued[T](Protocol):
    @property
    def value(self) -> T: ...

    @value.setter
    def value(self, value: T) -> None: ...
