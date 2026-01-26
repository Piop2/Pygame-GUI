from __future__ import annotations

from collections import defaultdict

from event.handler.base import BaseEventHandler
from model.event import InputEvent


class EventDispatcher:
    def __init__(self) -> None:

        self._handlers: dict[type[InputEvent], set[BaseEventHandler]] = defaultdict(set)

    def add_handler(self, handler: BaseEventHandler) -> None:
        self._handlers[handler.handled_event_type].add(handler)

    def remove_handler(self, handler: BaseEventHandler) -> None:
        self._handlers[handler.handled_event_type].remove(handler)

    def dispatch(self, event: InputEvent) -> bool:
        processed = False

        for handler in self._handlers[type(event)]:
            if handler.handle_event(event):
                processed = True

        return processed
