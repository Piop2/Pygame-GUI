from __future__ import annotations

from collections import defaultdict
from typing import Optional

from core.canvas_item import CanvasItem
from event.handler.base import BaseEventHandler
from model.event import InputEvent


class EventDispatcher:
    def __init__(self) -> None:

        self._handlers: dict[type[InputEvent], set[BaseEventHandler]] = defaultdict(set)

    def add_handler(self, handler: BaseEventHandler) -> None:
        self._handlers[handler.handled_event_type].add(handler)

    def remove_handler(self, handler: BaseEventHandler) -> None:
        self._handlers[handler.handled_event_type].remove(handler)

    def dispatch(self, view: CanvasItem, event: InputEvent) -> bool:
        processed = False

        event_type: Optional[type[InputEvent]] = None
        for key in self._handlers:
            if isinstance(event, key):
                event_type = key
                break

        if event_type is None:
            return False

        for handler in self._handlers[event_type]:
            if handler.handle_event(view, event):
                processed = True

        return processed
