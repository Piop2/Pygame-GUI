from __future__ import annotations

from pygame import Surface

from view.base import View


class ImageView(View):
    def __init__(self, image: Surface) -> None:
        super().__init__()

        self.style.width = image.width
        self.style.height = image.height

        self._image = image

    def _draw(self, surface: Surface) -> None:
        surface.blit(self._image, (0, 0))
