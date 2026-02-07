from __future__ import annotations

import pygame.transform
from pygame.surface import Surface

from view._valued import Valued
from view.button import ButtonView


class ImageButtonView(ButtonView, Valued[Surface]):
    def __init__(self, image: Surface) -> None:
        super().__init__()

        self._value = image
        return

    def _draw(self, surface: Surface) -> None:
        surface.blit(pygame.transform.scale(self._value, surface.size), (0, 0))
        return
