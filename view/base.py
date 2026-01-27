from __future__ import annotations

from copy import copy

import pygame.draw
import pygame.mask
from pygame.constants import SRCALPHA, BLEND_RGBA_MULT
from pygame.surface import Surface

from core.canvas_item import CanvasItem
from core.node import Node
from event.dispatcher import EventDispatcher
from event.handler import BaseEventHandler
from model.event import (
    InputEvent,
    MouseDownEvent,
    MouseUpEvent,
    MouseMotionEvent,
)


def _make_clear_surface(width: int, height: int) -> Surface:
    surface = Surface((width, height), flags=SRCALPHA)
    surface.fill((0, 0, 0, 0))
    return surface


class View(CanvasItem, Node):
    def __init__(self) -> None:
        super().__init__()

        self._enabled = True

        self._dispatcher = EventDispatcher()
        self._entered = False
        return

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        return

    def add_handler(self, handler: BaseEventHandler) -> None:
        self._dispatcher.add_handler(handler)
        return

    def remove_handler(self, handler: BaseEventHandler) -> None:
        self._dispatcher.remove_handler(handler)
        return

    def dispatch(self, event: InputEvent) -> bool:
        if self._style.width == 0 or self._style.height == 0:
            return False
        if not self._enabled:
            return False

        if self._dispatcher.dispatch(self, event):
            return True

        for child in self._children:
            if not isinstance(child, CanvasItem):
                continue

            child_event = copy(event)
            if isinstance(
                child_event, (MouseDownEvent, MouseUpEvent, MouseMotionEvent)
            ):
                child_event.pos.x -= self._transform.x
                child_event.pos.y -= self._transform.y

            if child.dispatch(child_event):
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
            if not isinstance(child, CanvasItem):
                continue

            child.render(view_surface)

        surface.blit(view_surface, (self.transform.x, self.transform.y))
        return
