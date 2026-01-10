from __future__ import annotations

from typing import Callable

from core.interact.base import Interactable
from model.style import Style
from model.event import MouseButton, MouseEvent, MouseDownEvent, MouseUpEvent, UIEvent

Position = tuple[int, int]

OnMouseDownCallback = Callable[[MouseButton, Position], bool]
OnMouseUpCallback = Callable[[MouseButton, Position], bool]
OnMouseHoverCallback = Callable[[Position], bool]
OnMouseEnterCallback = Callable[[], None]
OnMouseExitCallback = Callable[[], None]


class MouseInteractable(Interactable):
    _style: Style

    _on_mouse_down: OnMouseDownCallback
    _on_mouse_up: OnMouseUpCallback
    _on_mouse_hover: OnMouseHoverCallback
    _on_mouse_enter: OnMouseEnterCallback
    _on_mouse_exit: OnMouseExitCallback

    _entered: bool

    def _init_mouse_interaction(self) -> None:
        self._on_mouse_down = lambda key, position: False
        self._on_mouse_up = lambda key, position: False
        self._on_mouse_hover = lambda position: False
        self._on_mouse_enter = lambda: None
        self._on_mouse_exit = lambda: None

        self._entered = False

    def _process_mouse_event(self, event: UIEvent) -> bool:
        if not isinstance(event, MouseEvent):
            return False
        if not (
            0 <= event.x <= self._style.width and 0 <= event.y <= self._style.height
        ):
            if isinstance(event, MouseDownEvent):
                self.unfocus()

            if self._entered:
                self._entered = False
                self.mouse_exit()

            return False

        if not self._entered:
            self._entered = True
            self.mouse_enter()

        key = event.key
        position = (event.x, event.y)

        if isinstance(event, MouseDownEvent):
            return self.mouse_down(key, position)
        if isinstance(event, MouseUpEvent):
            return self.mouse_up(key, position)
        if isinstance(event, MouseEvent):
            return self.mouse_hover(position)

        raise RuntimeError

    def mouse_down(self, key: MouseButton, position: Position) -> bool:
        self.focus()
        return self._on_mouse_down(key, position)

    def mouse_up(self, key: MouseButton, position: Position) -> bool:
        return self._on_mouse_up(key, position)

    def mouse_hover(self, position: Position) -> bool:
        return self._on_mouse_hover(position)

    def mouse_enter(self) -> None:
        return self._on_mouse_enter()

    def mouse_exit(self) -> None:
        return self._on_mouse_exit()

    def on_mouse_down(self, callback: OnMouseDownCallback) -> None:
        self._on_mouse_down = callback

    def on_mouse_up(self, callback: OnMouseUpCallback) -> None:
        self._on_mouse_up = callback

    def on_mouse_hover(self, callback: OnMouseHoverCallback) -> None:
        self._on_mouse_hover = callback

    def on_mouse_enter(self, callback: OnMouseEnterCallback) -> None:
        self._on_mouse_enter = callback

    def on_mouse_exit(self, callback: OnMouseExitCallback) -> None:
        self._on_mouse_exit = callback
