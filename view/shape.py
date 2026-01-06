from __future__ import annotations

from pygame import Surface

from core.view import View


class RectView(View):
    def _draw(self, surface: Surface) -> None:
        surface.fill(self._style.background_color)
