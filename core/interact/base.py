from __future__ import annotations

from typing import Optional

from model.event import UIEvent


class Interactable:
    _focused: Optional[Interactable] = None

    def is_focused(self) -> bool:
        return self is Interactable._focused

    def focus(self) -> None:
        Interactable._focused = self

    def unfocus(self) -> None:
        if not self.is_focused():
            return

        Interactable._focused = None

    def _process_event(self, event: UIEvent) -> bool:
        return False

    def dispatch_event(self, event: UIEvent) -> bool: ...
