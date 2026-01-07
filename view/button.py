from __future__ import annotations

import pygame.draw

from core.view import View
from core.protocol.mouse import MouseInteractable
from model.event import UIEvent


class ButtonView(View, MouseInteractable):
    def __init__(self) -> None:
        super().__init__()

        self._init_mouse_interaction()

        self._on_mouse_enter = lambda: pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND
        )
        self._on_mouse_exit = lambda: pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_ARROW
        )

    def _process_event(self, event: UIEvent) -> bool:
        if self._process_mouse_event(event):
            return True

        return False
