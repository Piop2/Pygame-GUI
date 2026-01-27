from __future__ import annotations

from typing import TypeVar, Callable
from abc import ABC, abstractmethod

from core.canvas_item import CanvasItem
from model.event import InputEvent


E = TypeVar("E", bound=InputEvent)
Handler = Callable[[CanvasItem, E], bool]


class BaseEventHandler(ABC):
    def __init__(self) -> None:
        self._handler: dict[type[InputEvent], Handler] = {}

    @property
    @abstractmethod
    def handled_event_type(self) -> type[InputEvent]: ...

    def handle_event(self, view: CanvasItem, event: InputEvent) -> bool:
        try:
            return self._handler[type(event)](view, event)
        except KeyError:
            return False
