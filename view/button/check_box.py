from __future__ import annotations

import pygame.draw
from pygame import Surface

from event.handler import MouseHandler
from model import MouseButton
from view import View
from view._valued import Valued


class CheckBoxView(View, Valued[bool]):
    def __init__(self) -> None:
        super().__init__()

        self._style.background_color.update(255, 255, 255)

        self._value = False

        mouse_handler = MouseHandler()
        self._dispatcher.add_handler(mouse_handler)

        @mouse_handler.on_mouse_down
        def on_mouse_down(_view: CheckBoxView, button: MouseButton) -> bool:
            if button == MouseButton.LEFT:
                return True
            return False

        @mouse_handler.on_mouse_up
        def on_mouse_up(
            _view: CheckBoxView, button: MouseButton, _is_hit: bool
        ) -> bool:
            if button == MouseButton.LEFT:
                return True
            return False

        @mouse_handler.on_mouse_enter
        def on_mouse_enter(_view: CheckBoxView) -> None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return

        @mouse_handler.on_mouse_exit
        def on_mouse_exit(_view: CheckBoxView) -> None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return

        @mouse_handler.on_click
        def on_click(_view: CheckBoxView, button: MouseButton) -> None:
            if button == MouseButton.LEFT:
                self._value = not self._value
            return

        return

    def _draw(self, surface: Surface) -> None:
        width = int(self._style.width / 6)
        if self._value:
            width = 0

        pygame.draw.rect(surface, (0, 0, 0), ((0, 0), self._style.size), width)
        return
