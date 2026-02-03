from __future__ import annotations

from typing import Optional
from enum import Enum, auto

from util.timer import CountDownTimer
from view import View
from view._valued import Valued
from view.text import TextLayout

_BLINK_PERIOD = 1000


class CaretState(Enum):
    IDLE = auto()
    WORKING = auto()


class CaretView(View, Valued[int]):
    def __init__(self) -> None:
        super().__init__()
        self._style.width = 2
        self._style.background_color.update(0, 0, 0)
        self._value = 0

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

        if self._text_layout is not None:
            self._transform.pos = self._text_layout.caret_pos(self._value)
            self._style.height = self._text_layout.get_font_height()
        else:
            self._visible = False

        if self._visible:
            self._style.background_color.a = 255
        else:
            self._style.background_color.a = 0
