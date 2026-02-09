from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Transform:
    x: int = 0
    y: int = 0

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    @pos.setter
    def pos(self, value: tuple[int, int]) -> None:
        self.x = value[0]
        self.y = value[1]
        return
