from __future__ import annotations

from typing import Callable

from pygame.math import Vector2

from core.canvas_item import CanvasItem
from core.focus_manager import FOCUS_MANAGER
from event.handler.base import BaseEventHandler
from model.event import (
    MouseEvent,
    MouseUpEvent,
    MouseDownEvent,
    MouseMotionEvent,
    MouseScrollEvent,
    InputEvent,
)

OnMouseUpCallback = Callable[[CanvasItem, int, Vector2], bool]
OnMouseDownCallback = Callable[[CanvasItem, int, Vector2], bool]
OnMouseMotionCallback = Callable[[CanvasItem, Vector2], bool]
OnMouseScrollCallback = Callable[[CanvasItem, Vector2], bool]
OnMouseEnterCallback = Callable[[CanvasItem], None]
OnMouseExitCallback = Callable[[CanvasItem], None]
# OnClickCallback = Callable[[CanvasItem, int], bool]


class MouseHandler(BaseEventHandler):
    def __init__(self) -> None:
        super().__init__()

        self._on_mouse_up: OnMouseUpCallback = lambda v, k, p: False
        self._on_mouse_down: OnMouseDownCallback = lambda v, k, p: False
        self._on_mouse_motion: OnMouseMotionCallback = lambda v, p: False
        self._on_mouse_scroll: OnMouseScrollCallback = lambda v, d: False
        self._on_mouse_enter: OnMouseEnterCallback = lambda v: None
        self._on_mouse_exit: OnMouseExitCallback = lambda v: None
        # self._on_click: OnClickCallback = lambda v, k: False

        self._handler = {
            MouseUpEvent: self.mouse_up,
            MouseDownEvent: self.mouse_down,
            MouseMotionEvent: self.mouse_motion,
            MouseScrollEvent: self.mouse_scroll,
        }

        # self._last_pressed_key: Optional[int] = None
        self._entered = False
        return

    @property
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

    def mouse_up(self, view: CanvasItem, event: MouseUpEvent) -> bool:
        # if event.key == self._last_pressed_key:
        #     self.click()
        # else:
        #     self._last_pressed_key = None

        if not self._entered:
            return False

        return self._on_mouse_up(view, event.key, event.pos)

    def mouse_down(self, view: CanvasItem, event: MouseDownEvent) -> bool:
        # self._last_pressed_key = event.key

        if not self._entered:
            return False

        FOCUS_MANAGER.focus(view)
        return self._on_mouse_down(view, event.key, event.pos)

    def mouse_motion(self, view: CanvasItem, event: MouseMotionEvent) -> bool:
        is_hit = view.hit_test(event.pos.x, event.pos.y)

        if (not self._entered) and is_hit:
            self.mouse_enter(view)
            self._entered = True
        elif self._entered and (not is_hit):
            self.mouse_exit(view)
            self._entered = False

        if not self._entered:
            return False

        return self._on_mouse_motion(view, event.pos)

    def mouse_scroll(self, view: CanvasItem, event: MouseScrollEvent) -> bool:
        if not self._entered:
            return False

        return self._on_mouse_scroll(view, event.delta)

    def mouse_enter(self, view: CanvasItem) -> None:
        return self._on_mouse_enter(view)

    def mouse_exit(self, view: CanvasItem) -> None:
        # self._last_pressed_key = None

        return self._on_mouse_exit(view)

    # def click(self) -> bool:
    #     return self._on_click(self._view, self._last_pressed_key)
