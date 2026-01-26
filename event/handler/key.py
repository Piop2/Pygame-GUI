from __future__ import annotations

from typing import Callable

from core.view import View
from event.handler.base import BaseEventHandler
from model.event import InputEvent, KeyEvent, KeyDownEvent, KeyUpEvent, TextInputEvent

OnKeyDownCallback = Callable[[View, int], bool]
OnKeyUpCallback = Callable[[View, int], bool]
OnTextInput = Callable[[View, str], bool]


class KeyHandler(BaseEventHandler):
    def __init__(self, view: View) -> None:
        super().__init__(view)

        self._on_key_down = lambda v, k: False
        self._on_key_up = lambda v, k: False
        self._on_text_input = lambda v, t: False

        self._handler = {
            KeyDownEvent: self.key_down,
            KeyUpEvent: self.key_up,
            TextInputEvent: self.text_input,
        }

    def handled_event_type(self) -> type[InputEvent]:
        return KeyEvent

    def on_key_down(self, callback: OnKeyDownCallback) -> None:
        self._on_key_down = callback

    def on_key_up(self, callback: OnKeyUpCallback) -> None:
        self._on_key_up = callback

    def on_text_input(self, callback: OnTextInput) -> None:
        self._on_text_input = callback

    def key_down(self, event: KeyDownEvent) -> bool:
        return self._on_key_down(self._view, event.key)

    def key_up(self, event: KeyUpEvent) -> bool:
        return self._on_key_up(self._view, event.key)

    def text_input(self, event: TextInputEvent) -> bool:
        return self._on_text_input(self._view, event.text)
