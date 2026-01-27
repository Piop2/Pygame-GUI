from __future__ import annotations

from copy import copy
from dataclasses import dataclass

import pygame.transform
from pygame import Surface

from core.node import RootNode
from core.canvas_item import CanvasItem
from model.event import InputEvent, MouseDownEvent, MouseUpEvent, MouseMotionEvent


@dataclass(frozen=True)
class Viewport:
    size: tuple[int, int]
    scale: float = 1.0


class Screen(CanvasItem, RootNode):
    def __init__(self, viewport: Viewport, position: tuple[int, int] = (0, 0)) -> None:
        super().__init__()

        self.viewport: Viewport = viewport

        self._transform.x = position[0]
        self._transform.y = position[1]

    def dispatch(self, event: InputEvent) -> None:
        """dispatch a single pygame event to all nodes"""
        for child in self._children:
            if not isinstance(child, CanvasItem):
                continue

            child_event = copy(event)
            if isinstance(
                child_event, (MouseDownEvent, MouseUpEvent, MouseMotionEvent)
            ):
                child_event.pos.x -= child.transform.x
                child_event.pos.y -= child.transform.y

            if child.dispatch(child_event):
                return

    def update(self, delta_ms: int) -> None:
        """update all nodes"""

        worklist = self._children.copy()
        while worklist:
            current = worklist.pop()

            children = current.get_children()
            if children:
                worklist.extend(children)

            if isinstance(current, CanvasItem):
                current.update(delta_ms)

    def render(self, surface: Surface) -> None:
        """render screen"""
        screen_surface = Surface(self.viewport.size)
        screen_surface.fill(self._style.background_color)

        for child in self._children:
            if not isinstance(child, CanvasItem):
                continue

            child.render(screen_surface)

        surface.blit(
            pygame.transform.scale_by(screen_surface, self.viewport.scale), (0, 0)
        )
