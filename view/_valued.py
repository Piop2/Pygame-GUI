from __future__ import annotations

from typing import Protocol


class Valued[T](Protocol):
    _value: T

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        self._value = value
