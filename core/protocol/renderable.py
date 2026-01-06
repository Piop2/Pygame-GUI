from __future__ import annotations

from typing import Protocol, runtime_checkable

from pygame import Surface


@runtime_checkable
class Renderable(Protocol):
    def _draw(self, surface: Surface) -> None: ...

    def _apply_style(self, surface: Surface) -> None: ...

    def render(self, surface: Surface) -> None: ...
