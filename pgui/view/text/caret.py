from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from pygame import Surface

from pgui.util.timer import CountDownTimer
from pgui.view import View
from pgui.view._valued import Valued
from pgui.view.text import TextLayout

_BLINK_PERIOD = 1000


class CaretState(Enum):
    IDLE = auto()
    WORKING = auto()


@dataclass
class CaretPos:
    start: int
    end: int

    def has_selection(self) -> bool:
        return self.start != self.end

    def normalized(self) -> tuple[int, int]:
        if self.start <= self.end:
            return self.start, self.end
        return self.end, self.start


class CaretView(View, Valued[CaretPos]):
    def __init__(self) -> None:
        super().__init__()
        self._style.width = 2
        self._style.background_color.update(0, 0, 0, 0)

        self._value = CaretPos(0, 0)

        self._text_layout: Optional[TextLayout] = None

        self._state: CaretState = CaretState.IDLE
        self._timer = CountDownTimer(_BLINK_PERIOD)

        self._visible = False
        return

    @property
    def text_layout(self) -> Optional[TextLayout]:
        return self._text_layout

    @text_layout.setter
    def text_layout(self, value: Optional[TextLayout]) -> None:
        self._text_layout = value
        return

    @property
    def state(self) -> CaretState:
        return self._state

    @state.setter
    def state(self, value: CaretState) -> None:
        self._state = value
        return

    def update(self, delta: int) -> None:
        has_selection = self.value.has_selection()
        match self._state:
            case CaretState.IDLE:
                if self._timer.is_done():
                    self._visible = not self._visible
                    self._timer.reset()

                self._timer.update(delta)
            case CaretState.WORKING:
                self._state = CaretState.IDLE
                self._visible = True
                self._timer.reset()

        if has_selection:
            self._visible = True

        if self._text_layout is not None:
            self._style.height = self._text_layout.get_font_height()

            if self.value.has_selection():
                start, end = self.value.normalized()

                start_pos = self._text_layout.caret_pos(start)
                self._transform.pos = start_pos
                self._style.width = self._text_layout.caret_pos(end)[0] - start_pos[0]
            else:
                self._transform.pos = self._text_layout.caret_pos(self._value.end)
                self._style.width = 2
        else:
            self._visible = False
        return

    def _draw(self, surface: Surface) -> None:
        if not self._visible:
            return

        surface.fill("black")

        if not self.value.has_selection():
            return

        start, end = self.value.normalized()
        surface.blit(
            self._text_layout.font.render(
                self._text_layout.text[start:end], True, (255, 255, 255)
            ),
            (0, 0),
        )
        return
