from __future__ import annotations

from typing import Optional


class Node:
    def __init__(self) -> None:
        self._parent: Optional[Node] = None
        self._children: list[Node] = []
        return

    def get_children(self) -> tuple[Node, ...]:
        return tuple(self._children)

    def get_parent(self) -> Optional[Node]:
        return self._parent

    def _set_parent(self, new: Optional[Node]) -> None:
        self._parent = new
        return

    def add_node(self, node: Node) -> None:
        if node is self:
            raise RuntimeError

        node._set_parent(self)
        self._children.append(node)
        return

    def remove_node(self, node: Node) -> None:
        node._set_parent(None)
        self._children.remove(node)
        return
