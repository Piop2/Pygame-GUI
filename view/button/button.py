from __future__ import annotations

import pygame.draw

from event.handler import MouseHandler
from view.base import View


class ButtonView(View):
    def __init__(self) -> None:
        super().__init__()

        mouse_handler = MouseHandler()
        self._dispatcher.add_handler(mouse_handler)

        mouse_handler.on_mouse_enter(
            lambda v: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        )
        mouse_handler.on_mouse_exit(
            lambda v: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        )
        return
