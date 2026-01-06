from __future__ import annotations

from typing import Protocol, runtime_checkable

from model.transform import Transform


@runtime_checkable
class Transformed(Protocol):
    _transform = Transform()

    @property
    def transform(self) -> Transform:
        return self._transform
