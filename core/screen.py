from __future__ import annotations

from copy import copy
from dataclasses import dataclass

import pygame.transform
from pygame import Surface, Vector2

from core.node import RootNode
from core.view import View
from model.event import InputEvent, MouseDownEvent, MouseUpEvent, MouseMotionEvent
from model.style import Style


@dataclass(frozen=True)
class Viewport:
    size: tuple[int, int]
    scale: float = 1.0


class Screen(RootNode):
    def __init__(self, viewport: Viewport, position: tuple[int, int] = (0, 0)) -> None:
        super().__init__()

        self._style = Style()

        self.viewport: Viewport = viewport
        self._position: Vector2 = Vector2(position)

    @property
    def style(self) -> Style:
        return self._style

    @style.setter
    def style(self, value: Style) -> None:
        self._style = value

    @property
    def position(self) -> Vector2:
        return self._position

    def dispatch(self, event: InputEvent) -> None:
        """dispatch a single pygame event to all nodes"""

        for child in self._children:
            if not isinstance(child, View):
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

            if isinstance(current, View):
                current.update(delta_ms)

    def render(self, surface: Surface) -> None:
        """render screen"""
        screen_surface = Surface(self.viewport.size)
        screen_surface.fill(self._style.background_color)

        for child in self._children:
            if not isinstance(child, View):
                continue

            child.render(screen_surface)

        surface.blit(
            pygame.transform.scale_by(screen_surface, self.viewport.scale), (0, 0)
        )
