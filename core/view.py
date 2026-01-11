from __future__ import annotations

from copy import copy

import pygame.draw
import pygame.mask
from pygame.surface import Surface
from pygame.constants import SRCALPHA, BLEND_RGBA_MULT

from core.node import Node
from core.interface.renderable import Renderable
from core.interface.updatable import Updatable
from core.interact.base import Interactable
from core.interface.styled import Styled
from core.interface.transformed import Transformed
from model.event import UIEvent, MouseEvent
from model.style import Style
from model.transform import Transform


def _make_clear_surface(width: int, height: int) -> Surface:
    surface = Surface((width, height), flags=SRCALPHA)
    surface.fill((0, 0, 0, 0))
    return surface


class View(Node, Renderable, Updatable, Interactable, Styled, Transformed):
    def __init__(self):
        super().__init__()

        self._style = Style()
        self._transform = Transform()

        self._enabled: bool = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        return

    def dispatch_event(self, event: UIEvent) -> bool:
        if self._style.width == 0 or self._style.height == 0:
            return False
        if not self._enabled:
            return False

        if self._process_event(event):
            return True

        for child in self._children:
            if not isinstance(child, Interactable):
                continue

            child_event = copy(event)
            if isinstance(child_event, MouseEvent):
                child_event.x -= self._transform.x
                child_event.y -= self._transform.y

            if child.dispatch_event(child_event):
                return True

        return False

    def update(self, delta: int) -> None:
        # Implement me
        return

    def _draw(self, surface: Surface) -> None:
        # Implement me
        return

    def _apply_style(self, surface: Surface) -> Surface:
        if self._style.width == 0 or self._style.height == 0:
            return surface

        clip_mask = _make_clear_surface(self._style.width, self._style.height)
        pygame.draw.rect(
            clip_mask,
            color=(255, 255, 255, 255),
            rect=((0, 0), (self._style.width, self._style.height)),
            border_top_left_radius=self._style.border_top_left_radius,
            border_top_right_radius=self._style.border_top_right_radius,
            border_bottom_left_radius=self._style.border_bottom_left_radius,
            border_bottom_right_radius=self._style.border_bottom_right_radius,
        )

        content_surface = _make_clear_surface(self._style.width, self._style.height)
        content_surface.fill(self._style.background_color)
        content_surface.blit(surface)

        styled_surface = content_surface
        styled_surface.blit(clip_mask, (0, 0), special_flags=BLEND_RGBA_MULT)
        return styled_surface

    def render(self, surface: Surface) -> None:
        content_surface = _make_clear_surface(self._style.width, self._style.height)
        self._draw(content_surface)

        view_surface = self._apply_style(content_surface)

        for child in self._children:
            if not isinstance(child, Renderable):
                continue

            child.render(view_surface)

        surface.blit(view_surface, (self.transform.x, self.transform.y))
        return
