from __future__ import annotations

from typing import Callable

from core.focus_manager import FOCUS_MANAGER
from core.canvas_item import CanvasItem
from event.handler.base import BaseEventHandler
from model.event import InputEvent, KeyEvent, KeyDownEvent, KeyUpEvent, TextInputEvent

OnKeyDownCallback = Callable[[CanvasItem, int], bool]
OnKeyUpCallback = Callable[[CanvasItem, int], bool]
OnTextInput = Callable[[CanvasItem, str], None]


class KeyHandler(BaseEventHandler):
    def __init__(self) -> None:
        super().__init__()

        self._on_key_down = lambda v, k: False
        self._on_key_up = lambda v, k: False
        self._on_text_input = lambda v, t: None

        self._handler = {
            KeyDownEvent: self.key_down,
            KeyUpEvent: self.key_up,
            TextInputEvent: self.text_input,
        }
        return

    @property
    def handled_event_type(self) -> type[InputEvent]:
        return KeyEvent

    def on_key_down(self, callback: OnKeyDownCallback) -> None:
        self._on_key_down = callback
        return

    def on_key_up(self, callback: OnKeyUpCallback) -> None:
        self._on_key_up = callback
        return

    def on_text_input(self, callback: OnTextInput) -> None:
        self._on_text_input = callback
        return

    def key_down(self, view: CanvasItem, event: KeyDownEvent) -> bool:
        return self._on_key_down(view, event.key)

    def key_up(self, view: CanvasItem, event: KeyUpEvent) -> bool:
        return self._on_key_up(view, event.key)

    def text_input(self, view: CanvasItem, event: TextInputEvent) -> bool:
        if not FOCUS_MANAGER.is_focused(view):
            return False

        self._on_text_input(view, event.text)
        return True
