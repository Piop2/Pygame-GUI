from __future__ import annotations

from copy import copy
from dataclasses import dataclass

import pygame.transform
from pygame import Event, Surface, Vector2
from pygame.locals import MOUSEBUTTONUP, MOUSEMOTION

from core.view import View
from core.node import RootNode
from core.event_factory import EVENT_FACTORY
from core.protocol.interactable import Interactable
from core.protocol.renderable import Renderable
from core.protocol.updatable import Updatable
from core.protocol.styled import Styled
from model.event import UIEvent, MouseEvent
from model.style import Style


@dataclass(frozen=True)
class Viewport:
    size: tuple[int, int]
    scale: float = 1.0


class Screen(RootNode, Styled):
    def __init__(self, viewport: Viewport, position: tuple[int, int] = (0, 0)) -> None:
        super().__init__()

        self._style = Style()

        self.viewport: Viewport = viewport
        self._position: Vector2 = Vector2(position)

    @property
    def position(self) -> Vector2:
        return self._position

    def dispatch_event(self, event: Event) -> None:
        """dispatch a single pygame event to all nodes"""

        ui_event: UIEvent
        if MOUSEMOTION <= event.type <= MOUSEBUTTONUP:
            ui_event = EVENT_FACTORY.make_mouse_event(event)
        else:
            return

        for child in self._children:
            if not isinstance(child, View):
                continue
            if not isinstance(child, Interactable):
                continue

            child_event = copy(ui_event)
            if isinstance(child_event, MouseEvent):
                child_event.x -= child.transform.x
                child_event.y -= child.transform.y

            if child.dispatch_event(child_event):
                return

    def update(self, delta_ms: int) -> None:
        """update all nodes"""

        worklist = self._children.copy()
        while worklist:
            current = worklist.pop()

            children = current.get_children()
            if children:
                worklist.extend(children)

            if isinstance(current, Updatable):
                current.update(delta_ms)

    def render(self, surface: Surface) -> None:
        """render screen"""
        screen_surface = Surface(self.viewport.size)
        screen_surface.fill(self._style.background_color)

        for child in self._children:
            if not isinstance(child, Renderable):
                continue

            child.render(screen_surface)

        surface.blit(
            pygame.transform.scale_by(screen_surface, self.viewport.scale), (0, 0)
        )
