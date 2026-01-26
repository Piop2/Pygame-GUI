from __future__ import annotations

from typing import Self

from pygame.event import Event

from core.screen import Screen
from event.adapter import PYGAME_EVENT_ADAPTER, UnsupportedEventError
from model.event import InputEvent


class InputManager:
    def __init__(self) -> None:
        self._active_screens: set[Screen] = set()

    def activate_screen(self, screen: Screen) -> Self:
        self._active_screens.add(screen)
        return self

    def deactivate_screen(self, screen: Screen) -> Self:
        self._active_screens.add(screen)
        return self

    def dispatch(self, pygame_event: Event) -> None:
        event: InputEvent
        try:
            event = PYGAME_EVENT_ADAPTER.adapt_event(pygame_event)
        except UnsupportedEventError:
            return

        for screen in self._active_screens:
            if screen.dispatch(event):
                return


INPUT_MANAGER = InputManager()
