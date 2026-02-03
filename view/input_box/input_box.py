from __future__ import annotations

import re
from enum import Enum, auto

import pygame.mouse
import pygame.scrap
from pygame.constants import (
    K_v,
    K_BACKSPACE,
    K_RETURN,
    K_LCTRL,
    K_RIGHT,
    K_LEFT,
    SYSTEM_CURSOR_IBEAM,
    SYSTEM_CURSOR_ARROW,
)

from core.focus_manager import FOCUS_MANAGER
from event.handler import MouseHandler, KeyHandler
from model import MouseButton
from util.timer import CountDownTimer
from view import View
from view._valued import Valued
from view.text import TextView, ContentAlign
from view.text.caret import CaretView, CaretState

_INITIAL_COOLDOWN = 500
_REPEAT_COOLDOWN = 10


class _RemovalState(Enum):
    IDLE = auto()
    INITIAL_COOLDOWN = auto()

    REMOVING = auto()
    REPEAT_COOLDOWN = auto()


class InputBoxView(View, Valued[str]):
    def __init__(self) -> None:
        super().__init__()

        self._removal_state = _RemovalState.IDLE
        self._initial_timer = CountDownTimer(_INITIAL_COOLDOWN)
        self._repeat_timer = CountDownTimer(_REPEAT_COOLDOWN)

        self._pattern: str = ""

        self._ctrl_pressed = False

        self._caret_index = 0

        # ---------- Child Views ---------- #
        # Text View
        self._text_view = TextView()
        self._text_view.content_align = ContentAlign.MIDDLE_LEFT

        # CaretView
        self._caret_view = CaretView()

        self._children = [self._text_view, self._caret_view]

        mouse_handler = MouseHandler()
        key_handler = KeyHandler()
        self.add_handler(mouse_handler)
        self.add_handler(key_handler)

        @mouse_handler.on_mouse_down
        def on_mouse_down(_view: View, button: MouseButton) -> bool:
            if button == MouseButton.LEFT:
                return True

            return False

        @mouse_handler.on_mouse_enter
        def on_mouse_enter(_view: View) -> None:
            pygame.mouse.set_cursor(SYSTEM_CURSOR_IBEAM)
            return

        @mouse_handler.on_mouse_exit
        def on_mouse_exit(_view: View) -> None:
            pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
            return

        @key_handler.on_text_input
        def on_text_input(_view: View, text: str) -> None:
            self._input_text(text)
            return

        @key_handler.on_key_down
        def on_key_down(_view: View, key: int) -> bool:
            if key == K_BACKSPACE:
                if not self._text_view.value:
                    return True

                self._remove_text()

                self._removal_state = _RemovalState.INITIAL_COOLDOWN
                self._initial_timer.reset()
                return True

            if key == K_RETURN:
                FOCUS_MANAGER.unfocus(self)
                return True

            if key == K_LCTRL:
                self._ctrl_pressed = True
                return False

            if key == K_v:
                self._input_text(pygame.scrap.get_text())
                return True

            if key == K_RIGHT:
                self._set_caret_index(self._caret_index + 1)
                return True
            if key == K_LEFT:
                self._set_caret_index(self._caret_index - 1)
                return True

            return False

        @key_handler.on_key_up
        def on_key_up(_view: View, key: int) -> bool:
            if key == K_BACKSPACE:
                self._removal_state = _RemovalState.IDLE
                return False

            if key == K_LCTRL:
                self._ctrl_pressed = False
                return False

            return False

        return

    @property
    def value(self) -> str:
        return self._text_view.value

    @value.setter
    def value(self, value: str) -> None:
        self._text_view.value = value
        return

    @property
    def text_view(self) -> TextView:
        return self._text_view

    @property
    def pattern(self) -> str:
        return self._pattern

    @pattern.setter
    def pattern(self, value: str) -> None:
        self._pattern = value
        return

    def update(self, delta: int) -> None:
        self._text_view.style.size = self.style.size

        match self._removal_state:
            case _RemovalState.IDLE:
                pass

            case _RemovalState.INITIAL_COOLDOWN:
                if self._initial_timer.is_done():
                    self._removal_state = _RemovalState.REMOVING

                self._initial_timer.update(delta)

            case _RemovalState.REMOVING:
                self._remove_text()

                self._removal_state = _RemovalState.REPEAT_COOLDOWN
                self._repeat_timer.reset()

            case _RemovalState.REPEAT_COOLDOWN:
                if self._repeat_timer.is_done():
                    self._removal_state = _RemovalState.REMOVING

                self._repeat_timer.update(delta)

        if FOCUS_MANAGER.is_focused(self):
            self._caret_view.text_layout = self._text_view.layout()
        else:
            self._caret_view.text_layout = None
        self._caret_view.value = self._caret_index
        self._caret_view.update(delta)
        return

    def _set_caret_index(self, value: int) -> None:
        if value > (text_length := len(self._text_view.value)):
            self._caret_index = text_length
            return

        if value < 0:
            self._caret_index = 0
            return

        self._caret_index = value
        return

    def _remove_text(self) -> None:
        if self._caret_index == 0:
            return

        if self._text_view.value:
            self._text_view.value = (
                self._text_view.value[: self._caret_index - 1]
                + self._text_view.value[self._caret_index :]
            )
        self._set_caret_index(self._caret_index - 1)
        self._caret_view.state = CaretState.WORKING
        return

    def _input_text(self, text: str) -> None:
        for character in text:
            candidate_text = (
                self._text_view.value[: self._caret_index + 1]
                + character
                + self._text_view.value[self._caret_index + 1 :]
            )

            if self._pattern == "":
                self._text_view.value = candidate_text
                self._set_caret_index(self._caret_index + 1)
                self._caret_view.state = CaretState.WORKING
                return

            # check pattern
            if re.fullmatch(self._pattern, candidate_text) is None:
                continue
            self._text_view.value = candidate_text
            self._set_caret_index(self._caret_index + 1)
            self._caret_view.state = CaretState.WORKING
        return
