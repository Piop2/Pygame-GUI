from __future__ import annotations

from dataclasses import dataclass

from pygame import Font, Surface, Color
from pygame.font import get_default_font
from pygame.math import Vector2

from pgui.view import View
from pgui.view._valued import Valued
from pgui.model import ContentAlign, calc_aligned_pos


@dataclass(frozen=True)
class TextLayout:
    font: Font
    size: tuple[int, int]

    _fit_content: bool
    _align: ContentAlign

    text: str

    def get_font_height(self) -> int:
        return self.font.get_height()

    def caret_pos(self, index: int) -> Vector2:
        x, y = 0, 0
        if not self._fit_content:
            x, y = calc_aligned_pos(
                self._align,
                self.size,
                self.font.size(self.text),
            )

        return Vector2(x + self.font.size(self.text[:index])[0], y)

    def get_caret_at(self, pos: Vector2) -> int:
        x, _y = 0, 0
        if not self._fit_content:
            x, _y = calc_aligned_pos(self._align, self.size, self.font.size(self.text))

        caret_index = 0
        total_width = x

        for text in self.text:
            text_width = self.font.size(text)[0]

            if pos.x <= total_width + text_width // 2:
                break
            total_width += text_width
            caret_index += 1

        return caret_index


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
        return

    def layout(self) -> TextLayout:
        return TextLayout(
            self._font_renderer,
            self._style.size,
            self._fit_content,
            self._content_align,
            self._value,
        )
