from __future__ import annotations

from typing import Callable

from pygame.math import Vector2

from core.focus_manager import FOCUS_MANAGER
from core.view import View
from event.handler.base import BaseEventHandler
from model.event import (
    MouseEvent,
    MouseUpEvent,
    MouseDownEvent,
    MouseMotionEvent,
    MouseScrollEvent,
    InputEvent,
    MouseEnterEvent,
    MouseExitEvent,
)

OnMouseUpCallback = Callable[[View, int, Vector2], bool]
OnMouseDownCallback = Callable[[View, int, Vector2], bool]
OnMouseMotionCallback = Callable[[View, Vector2], bool]
OnMouseScrollCallback = Callable[[View, Vector2], bool]
OnMouseEnterCallback = Callable[[View], bool]
OnMouseExitCallback = Callable[[View], bool]
# OnClickCallback = Callable[[View, int], bool]


class MouseHandler(BaseEventHandler):
    def __init__(self, view: View) -> None:
        super().__init__(view)

        self._on_mouse_up: OnMouseUpCallback = lambda v, k, p: False
        self._on_mouse_down: OnMouseDownCallback = lambda v, k, p: False
        self._on_mouse_motion: OnMouseMotionCallback = lambda v, p: False
        self._on_mouse_scroll: OnMouseScrollCallback = lambda v, d: False
        self._on_mouse_enter: OnMouseEnterCallback = lambda v: False
        self._on_mouse_exit: OnMouseExitCallback = lambda v: False
        # self._on_click: OnClickCallback = lambda v, k: False

        self._handler = {
            MouseUpEvent: self.mouse_up,
            MouseDownEvent: self.mouse_down,
            MouseMotionEvent: self.mouse_motion,
            MouseScrollEvent: self.mouse_scroll,
            MouseEnterEvent: self.mouse_enter,
            MouseExitEvent: self.mouse_exit,
        }

        # self._last_pressed_key: Optional[int] = None

    def handled_event_type(self) -> type[InputEvent]:
        return MouseEvent

    def on_mouse_up(self, callback: OnMouseUpCallback) -> None:
        self._on_mouse_up = callback

    def on_mouse_down(self, callback: OnMouseDownCallback) -> None:
        self._on_mouse_down = callback

    def on_mouse_motion(self, callback: OnMouseMotionCallback) -> None:
        self._on_mouse_motion = callback

    def on_mouse_scroll(self, callback: OnMouseScrollCallback) -> None:
        self._on_mouse_scroll = callback

    def on_mouse_enter(self, callback: OnMouseEnterCallback) -> None:
        self._on_mouse_enter = callback

    def on_mouse_exit(self, callback: OnMouseExitCallback) -> None:
        self._on_mouse_exit = callback

    # def on_click(self, callback: OnClickCallback) -> None:
    #     self._on_click = callback

    def mouse_up(self, event: MouseUpEvent) -> bool:
        # if event.key == self._last_pressed_key:
        #     self.click()
        # else:
        #     self._last_pressed_key = None

        return self._on_mouse_up(self._view, event.key, event.pos)

    def mouse_down(self, event: MouseDownEvent) -> bool:
        # self._last_pressed_key = event.key

        FOCUS_MANAGER.focus(self._view)
        return self._on_mouse_down(self._view, event.key, event.pos)

    def mouse_motion(self, event: MouseMotionEvent) -> bool:
        return self._on_mouse_motion(self._view, event.pos)

    def mouse_scroll(self, event: MouseScrollEvent) -> bool:
        return self._on_mouse_scroll(self._view, event.delta)

    def mouse_enter(self, _: MouseEnterEvent) -> bool:
        return self._on_mouse_enter(self._view)

    def mouse_exit(self, _: MouseExitEvent) -> bool:
        # self._last_pressed_key = None

        return self._on_mouse_exit(self._view)

    # def click(self) -> bool:
    #     return self._on_click(self._view, self._last_pressed_key)
