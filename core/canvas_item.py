from __future__ import annotations

from abc import ABC, abstractmethod

from pygame.surface import Surface

from model.event import InputEvent
from model.style import Style
from model.transform import Transform


class CanvasItem(ABC):
    def __init__(self) -> None:
        super().__init__()

        self._style = Style()
        self._transform = Transform()

    @property
    def style(self) -> Style:
        return self._style

    @style.setter
    def style(self, value: Style) -> None:
        self._style = value
        return

    @property
    def transform(self) -> Transform:
        return self._transform

    @transform.setter
    def transform(self, value: Transform) -> None:
        self._transform = value
        return

    def hit_test(self, x: int | float, y: int | float) -> bool:
        return 0 <= x <= self._style.width and 0 <= y <= self._style.height

    @abstractmethod
    def dispatch(self, event: InputEvent) -> bool: ...

    @abstractmethod
    def update(self, delta: int) -> None: ...

    @abstractmethod
    def render(self, surface: Surface) -> None: ...
