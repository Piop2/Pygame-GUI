from __future__ import annotations

from typing import Optional, cast, override

from pygame import Surface

from core.node import Node


class CanvasItem(Node):
    def __init__(self) -> None:
        super().__init__()

        self.x = 0
        self.y = 0
        return

    @property
    def screen_x(self) -> int:
        result: int = 0

        node: Optional[CanvasItem] = self
        while True:
            if node is None:
                break

            result += node.x
            node = node.get_parent()
        return result

    @property
    def screen_y(self) -> int:
        result: int = 0

        node: Optional[CanvasItem] = self
        while True:
            if node is None:
                break

            result += node.y
            node = node.get_parent()
        return result

    @property
    def screen_pos(self) -> tuple[int, int]:
        return self.screen_x, self.screen_y

    def update(self, delta: int) -> None:
        for child in self.get_children():
            child.update(delta)
        return

    def render(self, surface: Surface) -> None:
        for child in self.get_children():
            child.render(surface)
        return

    @override
    def add_node(self, node: CanvasItem) -> None:
        return super().add_node(node)

    @override
    def get_children(self) -> tuple[CanvasItem, ...]:
        return cast(tuple[CanvasItem, ...], tuple(self._children))

    @override
    def get_parent(self) -> Optional[CanvasItem]:
        return cast(CanvasItem, self._parent)

    @override
    def _set_parent(self, new: Optional[CanvasItem]) -> None:
        self._parent = new
        return
