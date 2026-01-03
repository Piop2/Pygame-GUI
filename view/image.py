from __future__ import annotations

from typing import override

from pygame import Surface

from core.view import View


class ImageView(View):
    def __init__(self, image: Surface) -> None:
        super().__init__()

        self.width = image.width
        self.height = image.height

        self.__image = image

    @override
    def render(self, surface: Surface) -> None:
        surface.blit(self.__image, self.screen_pos)
        return super().render(surface)
