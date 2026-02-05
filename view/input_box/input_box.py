from __future__ import annotations

import re
from enum import Enum, auto
from typing import Callable

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
from view import View
from view._valued import Valued
from view.text import TextView, ContentAlign
from view.text.caret import CaretView, CaretState
from view.input_box._action import Action


def _make_action(handler: Callable[[], None]) -> Action:
    _INITIAL_COOLDOWN_DURATION = 500
    _REPEAT_INTERVAL_DURATION = 10

    class State(Enum):
        ACTION_ONCE = auto()
        INITIAL_COOLDOWN = auto()

        REPEAT_ACTION = auto()
        REPEAT_INTERVAL = auto()

    action = Action[State]()
    action.set_action(State.ACTION_ONCE)

    @action.register_handler("press", State.ACTION_ONCE)
    def remove_once():
        handler()
        return State.INITIAL_COOLDOWN

    @action.register_handler(
        "press", State.INITIAL_COOLDOWN, _INITIAL_COOLDOWN_DURATION
    )
    def cooldown():
        return State.REPEAT_ACTION

    @action.register_handler("press", State.REPEAT_ACTION)
    def remove():
        handler()
        return State.REPEAT_INTERVAL

    @action.register_handler("press", State.REPEAT_INTERVAL, _REPEAT_INTERVAL_DURATION)
    def remove_cooldown():
        return State.REPEAT_ACTION

    @action.register_handler(
        "release",
        (
            State.ACTION_ONCE,
            State.INITIAL_COOLDOWN,
            State.REPEAT_ACTION,
            State.REPEAT_INTERVAL,
        ),
    )
    def reset():
        return State.ACTION_ONCE

    return action


class InputBoxView(View, Valued[str]):
    def __init__(self) -> None:
        super().__init__()

        self._pattern: str = ""

        self._ctrl_pressed = False

        self._caret_index = 0

        # ---------- Actions ---------- #
        self._removal_action = _make_action(lambda: self._remove_text())
        self._caret_right_action = _make_action(
            lambda: self._set_caret_index(self._caret_index + 1)
        )
        self._caret_left_action = _make_action(
            lambda: self._set_caret_index(self._caret_index - 1)
        )

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

                self._removal_action.press()
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
                self._caret_right_action.press()
                return True
            if key == K_LEFT:
                self._caret_left_action.press()
                return True

            return False

        @key_handler.on_key_up
        def on_key_up(_view: View, key: int) -> bool:
            if key == K_BACKSPACE:
                self._removal_action.release()
                return False

            if key == K_LCTRL:
                self._ctrl_pressed = False
                return False

            if key == K_RIGHT:
                self._caret_right_action.release()
                return True
            if key == K_LEFT:
                self._caret_left_action.release()
                return True

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

        self._removal_action.update(delta)
        self._caret_left_action.update(delta)
        self._caret_right_action.update(delta)

        if FOCUS_MANAGER.is_focused(self):
            self._caret_view.text_layout = self._text_view.layout()
        else:
            self._caret_view.text_layout = None
        self._caret_view.value = self._caret_index
        self._caret_view.update(delta)
        return

    def _set_caret_index(self, value: int) -> None:
        self._caret_view.state = CaretState.WORKING

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
        return

    def _input_text(self, text: str) -> None:
        for character in text:
            candidate_text = (
                self._text_view.value[: self._caret_index]
                + character
                + self._text_view.value[self._caret_index :]
            )

            if self._pattern == "":
                self._text_view.value = candidate_text
                self._set_caret_index(self._caret_index + 1)
                return

            # check pattern
            if re.fullmatch(self._pattern, candidate_text) is None:
                continue
            self._text_view.value = candidate_text
            self._set_caret_index(self._caret_index + 1)
        return
