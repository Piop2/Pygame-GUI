from __future__ import annotations

from pygame import Event
from pygame.locals import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    KEYDOWN,
    KEYUP,
    TEXTINPUT,
)

from model.event import (
    MouseEvent,
    MouseDownEvent,
    MouseUpEvent,
    MouseButton,
    KeyboardEvent,
    KeyboardEventType,
)


class __EventFactory:
    @staticmethod
    def make_mouse_event(event: Event) -> MouseEvent:
        if event.type == MOUSEBUTTONDOWN:
            return MouseDownEvent(event.button, event.pos[0], event.pos[1])

        if event.type == MOUSEBUTTONUP:
            return MouseUpEvent(event.button, event.pos[0], event.pos[1])

        if event.type == MOUSEMOTION:
            return MouseEvent(MouseButton.NONE, event.pos[0], event.pos[1])

        raise ValueError

    @staticmethod
    def make_keyboard_event(event: Event) -> KeyboardEvent:
        if event.type == KEYDOWN:
            return KeyboardEvent(KeyboardEventType.DOWN, event.key, "")
        if event.type == KEYUP:
            return KeyboardEvent(KeyboardEventType.UP, event.key, "")
        if event.type == TEXTINPUT:
            return KeyboardEvent(KeyboardEventType.INPUT, 0, event.text)

        raise ValueError


EVENT_FACTORY = __EventFactory()
