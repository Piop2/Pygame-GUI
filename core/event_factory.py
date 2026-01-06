from __future__ import annotations

from pygame import Event
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

from model.event import MouseEvent, MouseDownEvent, MouseUpEvent, MouseButton


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


EVENT_FACTORY = __EventFactory()
