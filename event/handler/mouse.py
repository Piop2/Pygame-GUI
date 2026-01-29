from __future__ import annotations

from typing import Callable, Optional
from enum import Enum, auto

from pygame.math import Vector2

from core.canvas_item import CanvasItem
from core.focus_manager import FOCUS_MANAGER
from event.handler.base import BaseEventHandler
from model import (
    MouseButton,
    MouseEvent,
    MouseUpEvent,
    MouseDownEvent,
    MouseMotionEvent,
    MouseScrollEvent,
    InputEvent,
)

OnMouseUpCallback = Callable[[CanvasItem, MouseButton, bool], bool]
OnMouseDownCallback = Callable[[CanvasItem, MouseButton], bool]
OnMouseMotionCallback = Callable[[CanvasItem, Vector2, bool], bool]
OnMouseScrollCallback = Callable[[CanvasItem, Vector2], bool]
OnMouseEnterCallback = Callable[[CanvasItem], None]
OnMouseExitCallback = Callable[[CanvasItem], None]
OnClickCallback = Callable[[CanvasItem, MouseButton], None]


class ClickState(Enum):
    IDLE = auto()
    PRESSED = auto()


class MouseHandler(BaseEventHandler):
    def __init__(self) -> None:
        super().__init__()

        self._on_mouse_up: OnMouseUpCallback = lambda v, b, i: False
        self._on_mouse_down: OnMouseDownCallback = lambda v, b: False
        self._on_mouse_motion: OnMouseMotionCallback = lambda v, p, i: False
        self._on_mouse_scroll: OnMouseScrollCallback = lambda v, d: False
        self._on_mouse_enter: OnMouseEnterCallback = lambda v: None
        self._on_mouse_exit: OnMouseExitCallback = lambda v: None
        self._on_click: OnClickCallback = lambda v, b: None

        self._handler = {
            MouseUpEvent: self.mouse_up,
            MouseDownEvent: self.mouse_down,
            MouseMotionEvent: self.mouse_motion,
            MouseScrollEvent: self.mouse_scroll,
        }

        self._click_state = ClickState.IDLE
        self._active_click_button: Optional[MouseButton] = None

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

    def on_click(self, callback: OnClickCallback) -> None:
        self._on_click = callback
        return

    def mouse_up(self, view: CanvasItem, event: MouseUpEvent) -> bool:
        if not FOCUS_MANAGER.is_focused(view):
            return False
        if not self._on_mouse_up(view, event.button, self._entered):
            return True

        # No handling needed: click_state is reset by on_mouse_exit
        # when mouse_up occurs outside a hit.

        if (
            self._click_state == ClickState.PRESSED
            and event.button == self._active_click_button
        ):
            self._on_click(view, self._active_click_button)

        self._click_state = ClickState.IDLE
        self._active_click_button = None
        return True

    def mouse_down(self, view: CanvasItem, event: MouseDownEvent) -> bool:
        if not self._entered:
            return False

        if not self._on_mouse_down(view, event.button):
            return False

        self._active_click_button = event.button
        self._click_state = ClickState.PRESSED

        FOCUS_MANAGER.focus(view)
        return True

    def mouse_motion(self, view: CanvasItem, event: MouseMotionEvent) -> bool:
        is_hit = view.hit_test(event.pos.x, event.pos.y)

        if (not self._entered) and is_hit:
            self.mouse_enter(view)
            self._entered = True
        elif self._entered and (not is_hit):
            self.mouse_exit(view)
            self._entered = False

        if FOCUS_MANAGER.is_focused(view) or self._entered:
            return self._on_mouse_motion(view, event.pos, self._entered)

        return False

    def mouse_scroll(self, view: CanvasItem, event: MouseScrollEvent) -> bool:
        if not self._entered:
            return False

        return self._on_mouse_scroll(view, event.delta)

    def mouse_enter(self, view: CanvasItem) -> None:
        return self._on_mouse_enter(view)

    def mouse_exit(self, view: CanvasItem) -> None:
        self._active_click_button = None
        self._click_state = ClickState.IDLE

        return self._on_mouse_exit(view)

    def click(self, view: CanvasItem) -> None:
        if self._active_click_button is None:
            raise RuntimeError

        self._on_click(view, self._active_click_button)
        return
