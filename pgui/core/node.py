from __future__ import annotations

from typing import Self


class Node:
    def __init__(self) -> None:
        super().__init__()

        self._children: list[Node] = []

    def get_children(self) -> tuple[Node, ...]:
        return tuple(self._children)

    def add_node(self, node: Node) -> Self:
        if node is self:
            raise RuntimeError
        if isinstance(node, RootNode):
            raise RuntimeError

        self._children.append(node)

        return self

    def remove_node(self, node: Node) -> Self:
        self._children.remove(node)

        return self


class RootNode(Node):
    def __init__(self) -> None:
        super().__init__()
        return
