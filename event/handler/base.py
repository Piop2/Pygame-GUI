from __future__ import annotations

from typing import TypeVar, Callable
from abc import ABC, abstractmethod

from core.view import View
from model.event import InputEvent


E = TypeVar("E", bound=InputEvent)
Handler = Callable[[E], bool]


class BaseEventHandler(ABC):
    def __init__(self, view: View) -> None:
        self._view = view
        self._handler: dict[type[InputEvent], Handler] = {}

    @property
    @abstractmethod
    def handled_event_type(self) -> type[InputEvent]: ...

    def handle_event(self, event: InputEvent) -> bool:
        try:
            return self._handler[type(event)](event)
        except KeyError:
            return False
