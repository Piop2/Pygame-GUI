from __future__ import annotations

import pygame.draw
from pygame import Surface

from core.view import View
from core.protocol.mouse import MouseInteractable
from model.event import UIEvent


class ButtonView(View, MouseInteractable):
    def __init__(self) -> None:
        super().__init__()

        self._init_mouse_interaction()

    def _draw(self, surface: Surface) -> None:
        pygame.draw.rect(
            surface,
            color=self._style.background_color,
            rect=((0, 0), (self._style.width, self._style.height)),
            border_top_left_radius=self._style.border_top_left_radius,
            border_top_right_radius=self._style.border_top_right_radius,
            border_bottom_left_radius=self._style.border_bottom_left_radius,
            border_bottom_right_radius=self._style.border_bottom_right_radius,
        )

    def process_event(self, event: UIEvent) -> bool:
        if self._process_mouse_event(event):
            return True

        return False
