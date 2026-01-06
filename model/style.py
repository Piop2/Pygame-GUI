from __future__ import annotations

from dataclasses import dataclass, field

from pygame import Color


@dataclass
class Style:
    width: int = 0
    height: int = 0

    background_color: Color = field(default_factory=lambda: Color(0, 0, 0))

    opacity: int = 255

    # border radius
    border_top_left_radius: int = 0
    border_top_right_radius: int = 0
    border_bottom_left_radius: int = 0
    border_bottom_right_radius: int = 0

    @property
    def border_radius(self) -> int:
        if (
            self.border_top_left_radius
            == self.border_top_right_radius
            == self.border_bottom_left_radius
            == self.border_bottom_right_radius
        ):
            return self.border_top_left_radius

        # idk...
        return -1

    @border_radius.setter
    def border_radius(self, new: int) -> None:
        self.border_top_left_radius = new
        self.border_top_right_radius = new
        self.border_bottom_left_radius = new
        self.border_bottom_right_radius = new
