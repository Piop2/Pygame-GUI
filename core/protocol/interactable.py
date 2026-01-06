from __future__ import annotations

from typing import Protocol, runtime_checkable

from model.event import UIEvent


@runtime_checkable
class Interactable(Protocol):
    def process_event(self, event: UIEvent) -> bool:
        return False

    def dispatch_event(self, event: UIEvent) -> bool: ...
