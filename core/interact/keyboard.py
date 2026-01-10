from __future__ import annotations


from typing import Callable

from core.interact.base import Interactable
from model.event import UIEvent, KeyboardEvent, KeyboardEventType


OnKeyDownCallback = Callable[[int], bool]
OnKeyUpCallback = Callable[[int], bool]
OnInputCallback = Callable[[str], None]


class KeyboardInteractable(Interactable):

    _on_key_down: OnKeyDownCallback
    _on_key_up: OnKeyUpCallback
    _on_input: OnInputCallback

    def _init_keyboard_interaction(self) -> None:
        self._on_key_down = lambda key: False
        self._on_key_up = lambda key: False
        self._on_input = lambda text: None

    def _process_keyboard_event(self, event: UIEvent) -> bool:
        if not isinstance(event, KeyboardEvent):
            return False
        if not self.is_focused():
            return False

        match event.type:
            case KeyboardEventType.DOWN:
                return self.key_down(event.key)
            case KeyboardEventType.UP:
                return self.key_up(event.key)
            case KeyboardEventType.INPUT:
                self.input(event.text)
                return True

    def key_down(self, key: int) -> bool:
        return self._on_key_down(key)

    def key_up(self, key: int) -> bool:
        return self._on_key_up(key)

    def input(self, text: str) -> None:
        self._on_input(text)

    def on_key_down(self, callback: OnKeyDownCallback) -> None:
        self._on_key_down = callback

    def on_key_up(self, callback: OnKeyUpCallback) -> None:
        self._on_key_up = callback

    def on_input(self, callback: OnInputCallback) -> None:
        self._on_input = callback
