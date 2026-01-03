from __future__ import annotations

from typing import override, cast, Optional

from pygame import Rect, Event

from core.canvas_item import CanvasItem


class View(CanvasItem):
    def __init__(self) -> None:
        super().__init__()

        self.width = 0
        self.height = 0
        return

    @property
    def rect(self) -> Rect:
        return Rect(self.screen_pos, (self.width, self.height))

    def contains(self, x: int, y: int) -> bool:
        return self.rect.collidepoint(x, y)

    def process(self, events: list[Event]) -> bool:
        for child in self.get_children():
            if child.process(events):
                return True
        return False

    @override
    def add_node(self, node: View) -> None:
        return super().add_node(node)

    @override
    def get_children(self) -> tuple[View, ...]:
        return cast(tuple[View, ...], tuple(self._children))

    @override
    def get_parent(self) -> Optional[View]:
        return self._parent

    @override
    def _set_parent(self, new: Optional[View]) -> None:
        self._parent = new
        return
