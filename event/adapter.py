from __future__ import annotations

from typing import Callable

from pygame.constants import MOUSEWHEEL
from pygame.event import Event, event_name
from pygame.math import Vector2
from pygame.locals import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    KEYDOWN,
    KEYUP,
    TEXTINPUT,
)

from model.event import (
    InputEvent,
    MouseDownEvent,
    MouseUpEvent,
    MouseMotionEvent,
    MouseScrollEvent,
    KeyDownEvent,
    KeyUpEvent,
    TextInputEvent,
)

PygameEventHandler = Callable[[Event], InputEvent]


class UnsupportedEventError(Exception):
    def __init__(self, event_type: int) -> None:
        super().__init__(f"Unsupported pygame event: {event_name(event_type)}")


class PygameEventAdapter:
    def __init__(self) -> None:
        self._handlers: dict[int, PygameEventHandler] = {
            KEYUP: lambda event: KeyUpEvent(event.key),
            KEYDOWN: lambda event: KeyDownEvent(event.key),
            TEXTINPUT: lambda event: TextInputEvent(event.text),
            MOUSEBUTTONUP: lambda event: MouseUpEvent(event.button, Vector2(event.pos)),
            MOUSEBUTTONDOWN: lambda event: MouseDownEvent(
                event.button, Vector2(event.pos)
            ),
            MOUSEMOTION: lambda event: MouseMotionEvent(Vector2(event.pos)),
            MOUSEWHEEL: lambda event: MouseScrollEvent(Vector2(event.x, event.y)),
        }

    def adapt_event(self, pygame_event: Event) -> InputEvent:
        try:
            return self._handlers[pygame_event.type](pygame_event)
        except KeyError:
            raise UnsupportedEventError(pygame_event.type)


PYGAME_EVENT_ADAPTER = PygameEventAdapter()
