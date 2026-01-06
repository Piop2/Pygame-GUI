from __future__ import annotations

from typing import Callable, Optional

from model.style import Style
from model.event import MouseButton, MouseEvent, MouseDownEvent, MouseUpEvent, UIEvent

Position = tuple[int, int]

OnMouseDownCallback = Callable[[MouseButton, Optional[Position]], bool]
OnMouseUpCallback = Callable[[MouseButton, Optional[Position]], bool]
OnMouseHoverCallback = Callable[[Optional[Position]], bool]


class MouseInteractable:
    _style: Style

    _on_mouse_down: OnMouseDownCallback
    _on_mouse_up: OnMouseUpCallback
    _on_mouse_hover: OnMouseHoverCallback

    def _init_mouse_interaction(self) -> None:
        self._on_mouse_down: OnMouseDownCallback = lambda key, position: False
        self._on_mouse_up: OnMouseUpCallback = lambda key, position: False
        self._on_mouse_hover: OnMouseHoverCallback = lambda position: False

    def _process_mouse_event(self, event: UIEvent) -> bool:
        if not isinstance(event, MouseEvent):
            return False

        key: MouseButton = event.key
        position: Optional[Position] = None

        if 0 <= event.x <= self._style.width and 0 <= event.y <= self._style.height:
            position = (event.x, event.y)

        if isinstance(event, MouseDownEvent):
            return self.mouse_down(key, position)
        if isinstance(event, MouseUpEvent):
            return self.mouse_up(key, position)
        if isinstance(event, MouseEvent):
            return self.mouse_hover(position)

        raise RuntimeError

    def mouse_down(self, key: MouseButton, position: Optional[Position]) -> bool:
        return self._on_mouse_down(key, position)

    def mouse_up(self, key: MouseButton, position: Optional[Position]) -> bool:
        return self._on_mouse_up(key, position)

    def mouse_hover(self, position: Optional[Position]) -> bool:
        return self._on_mouse_hover(position)

    def on_mouse_down(
        self, callback: Callable[[MouseButton, Optional[Position]], bool]
    ) -> None:
        self._on_mouse_down = callback

    def on_mouse_up(
        self, callback: Callable[[MouseButton, Optional[Position]], bool]
    ) -> None:
        self._on_mouse_up = callback

    def on_mouse_hover(self, callback: Callable[[Optional[Position]], bool]) -> None:
        self._on_mouse_hover = callback
