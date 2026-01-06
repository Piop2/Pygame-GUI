from __future__ import annotations

from copy import copy

from pygame import Surface, SRCALPHA

from core.node import Node
from core.protocol.renderable import Renderable
from core.protocol.updatable import Updatable
from core.protocol.interactable import Interactable
from core.protocol.styled import Styled
from core.protocol.transformed import Transformed
from model.event import UIEvent, MouseEvent
from model.style import Style
from model.transform import Transform


class View(Node, Renderable, Updatable, Interactable, Styled, Transformed):
    def __init__(self):
        super().__init__()

        self._style = Style()
        self._transform = Transform()

    def dispatch_event(self, event: UIEvent) -> bool:
        if self._style.width == 0 or self._style.height == 0:
            return False

        for child in self._children:
            if not isinstance(child, Interactable):
                continue

            child_event = copy(event)
            if isinstance(child_event, MouseEvent):
                child_event.x -= self._transform.x
                child_event.y -= self._transform.y

            if child.dispatch_event(child_event):
                return True

        return self.process_event(event)

    def update(self, delta: int) -> None:
        # Implement me
        return

    def _draw(self, surface: Surface) -> None:
        # Implement me
        return

    def _apply_style(self, surface: Surface) -> None:
        if self._style.width == 0 or self._style.height == 0:
            return

        return

    def render(self, surface: Surface) -> None:
        view_surface = Surface((self._style.width, self._style.height), flags=SRCALPHA)
        view_surface.fill((0, 0, 0, 0))

        self._draw(view_surface)
        self._apply_style(view_surface)

        for child in self._children:
            if not isinstance(child, Renderable):
                continue

            child.render(view_surface)

        surface.blit(view_surface, (self.transform.x, self.transform.y))
        return
