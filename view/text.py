from __future__ import annotations


from pygame import Font, Surface, Color
from pygame.font import get_default_font

from view import View
from view._valued import Valued
from model.align import ContentAlign, calc_aligned_pos


class TextView(View, Valued[str]):
    def __init__(self) -> None:
        super().__init__()

        self._style.background_color.a = 0

        self._value = ""

        self._font = get_default_font()
        self._font_size = 20
        self._font_color = Color(0, 0, 0)

        self._font_renderer = Font(self._font, self._font_size)

        self._fit_content = False
        self._content_align = ContentAlign.TOP_LEFT
        return

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value
        return

    @property
    def font(self) -> str:
        return self._font

    @font.setter
    def font(self, value: str) -> None:
        self._font = value
        self._font_renderer = Font(value, self._font_size)
        return

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        self._font_size = value
        self._font_renderer.set_point_size(value)
        return

    @property
    def font_color(self) -> Color:
        return self._font_color

    @font_color.setter
    def font_color(self, value: Color) -> None:
        self._font_color = value
        return

    @property
    def fit_content(self) -> bool:
        return self._fit_content

    @fit_content.setter
    def fit_content(self, value: bool) -> None:
        self._fit_content = value
        return

    @property
    def content_align(self) -> ContentAlign:
        return self._content_align

    @content_align.setter
    def content_align(self, value: ContentAlign) -> None:
        self._content_align = value
        return

    def update(self, _delta: int) -> None:
        if self._fit_content:
            self._style.size = self._font_renderer.size(self._value)
        return

    def _draw(self, surface: Surface) -> None:
        x, y = (0, 0)
        if not self._fit_content:
            x, y = calc_aligned_pos(
                self._content_align,
                self._style.size,
                self._font_renderer.size(self._value),
            )

        surface.blit(
            self._font_renderer.render(self._value, True, self._font_color), (x, y)
        )
