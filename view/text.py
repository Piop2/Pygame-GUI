from __future__ import annotations

from core.view import View

from pygame import Font, Surface, Color
from pygame.font import get_default_font


class TextView(View):
    def __init__(self) -> None:
        super().__init__()

        self._text = ""

        self._font = get_default_font()
        self._font_size = 20
        self._font_color = Color(0, 0, 0)

        self._font_renderer = Font(self._font, self._font_size)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

        # fix size
        size = self._font_renderer.size(self._text)
        self._style.width = size[0]
        self._style.height = size[1]

    @property
    def font(self) -> str:
        return self._font

    @font.setter
    def font(self, value: str) -> None:
        self._font = value
        self._font_renderer = Font(value, self._font_size)

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        self._font_size = value
        self._font_renderer.set_point_size(value)

        # fix size
        size = self._font_renderer.size(self._text)
        self._style.width = size[0]
        self._style.height = size[1]

    @property
    def font_color(self) -> Color:
        return self._font_color

    @font_color.setter
    def font_color(self, value: Color) -> None:
        self._font_color = value

    def _draw(self, surface: Surface) -> None:
        surface.blit(
            self._font_renderer.render(self._text, True, self._font_color), (0, 0)
        )
