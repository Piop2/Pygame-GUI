from __future__ import annotations

import re
from enum import Enum, auto
from typing import Callable, Optional, Literal

import pygame.mouse
import pygame.scrap
from pygame.constants import (
    K_a,
    K_c,
    K_v,
    K_z,
    K_BACKSPACE,
    K_RETURN,
    K_LCTRL,
    K_RIGHT,
    K_LEFT,
    K_LSHIFT,
    SYSTEM_CURSOR_IBEAM,
    SYSTEM_CURSOR_ARROW,
)
from pygame.math import Vector2

from pgui.core.focus_manager import FOCUS_MANAGER
from pgui.event.handler import MouseHandler, KeyHandler
from pgui.model import MouseButton
from pgui.view import View
from pgui.view._valued import Valued
from pgui.view.input_box._action import Action
from pgui.view.text import TextView, ContentAlign, TextLayout
from pgui.view.text.caret import CaretView, CaretState, CaretPos
from pgui.view.input_box.memento import Originator, Caretaker


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

        self._value = ""

        self._pattern: str = ""

        self._ctrl_pressed = False
        self._shift_pressed = False
        self._mouse_left_pressed = False

        # caret pos: (start_pos, end_pos)
        self._caret_pos = CaretPos(0, 0)
        self._dragging = False

        self._text_layout: Optional[TextLayout] = None

        # ---------- Memento ---------- #
        self._originator = Originator()
        self._caretaker = Caretaker(self._originator)
        self._make_backup()

        # ---------- Actions ---------- #
        self._removal_action = _make_action(lambda: self._remove_text())
        self._caret_right_action = _make_action(
            lambda: self._set_caret_pos(self._caret_pos.end + 1)
        )
        self._caret_left_action = _make_action(
            lambda: self._set_caret_pos(self._caret_pos.end - 1)
        )
        self._undo_action = _make_action(lambda: self._undo())

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
        def on_mouse_down(_view: View, button: MouseButton, pos: Vector2) -> bool:
            if button == MouseButton.LEFT:
                self._mouse_left_pressed = True
                self._set_caret_pos(self._text_layout.get_caret_at(pos))
                return True

            return False

        @mouse_handler.on_mouse_up
        def on_mouse_up(_view: View, button: MouseButton, _is_entered: bool) -> bool:
            if button == MouseButton.LEFT:
                self._mouse_left_pressed = False
                self._dragging = False
                return True

            return False

        @mouse_handler.on_mouse_motion
        def on_mouse_motion(_view: View, pos: Vector2, _is_entered: bool) -> bool:
            if self._mouse_left_pressed:
                self._dragging = True

            if self._dragging:
                self._set_caret_pos(self._text_layout.get_caret_at(pos))
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
                if self._caret_pos.has_selection():
                    self._remove_selected_text()
                    return True

                if self._ctrl_pressed:
                    last_caret_pos = self._caret_pos.end

                    self._move_caret_by_word("left")
                    self._caret_pos.start = last_caret_pos

                    self._remove_selected_text()
                    return True

                self._removal_action.press()
                return True

            if key == K_RETURN:
                FOCUS_MANAGER.unfocus(self)
                return True

            if key == K_LCTRL:
                self._ctrl_pressed = True
                return False

            if key == K_a:
                if self._ctrl_pressed:
                    self._caret_pos.start = 0
                    self._caret_pos.end = len(self._value)
                    return True
                return False

            if key == K_c and self._ctrl_pressed:
                pygame.scrap.put_text(self._value)
                return True

            if key == K_v and self._ctrl_pressed:
                self._input_text(pygame.scrap.get_text())
                return True

            if key == K_z and self._ctrl_pressed:
                self._undo_action.press()
                return True

            if key == K_RIGHT:
                if self._shift_pressed:
                    self._dragging = True

                if self._ctrl_pressed:
                    self._move_caret_by_word("right")
                    return True

                elif not self._dragging and self._caret_pos.has_selection():
                    self._set_caret_pos(self._caret_pos.end)
                    return True

                self._caret_right_action.press()
                return True

            if key == K_LEFT:
                if self._shift_pressed:
                    self._dragging = True

                if self._ctrl_pressed:
                    self._move_caret_by_word("left")
                    return True

                elif not self._dragging and self._caret_pos.has_selection():
                    self._set_caret_pos(self._caret_pos.start)
                    return True

                self._caret_left_action.press()
                return True

            if key == K_LSHIFT:
                self._shift_pressed = True
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

            if key == K_z:
                self._undo_action.release()
                return True

            if key == K_RIGHT:
                self._caret_right_action.release()
                return True
            if key == K_LEFT:
                self._caret_left_action.release()
                return True
            if key == K_LSHIFT:
                self._shift_pressed = False
                self._dragging = False
                return True

            return False

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
        self._text_view.value = self._value
        self._text_view.style.size = self.style.size
        self._text_layout = self.text_view.layout()

        self._removal_action.update(delta)
        self._caret_left_action.update(delta)
        self._caret_right_action.update(delta)
        self._undo_action.update(delta)

        if FOCUS_MANAGER.is_focused(self):
            self._caret_view.text_layout = self._text_layout
            self._caret_view.value = self._caret_pos
            self._caret_view.update(delta)
        else:
            self._caret_view.text_layout = None
        return

    def _set_caret_pos(self, pos: int) -> None:
        self._caret_view.state = CaretState.WORKING

        if pos > (text_length := len(self._value)):
            pos = text_length
        elif pos < 0:
            pos = 0

        if not self._dragging:
            self._caret_pos.start = pos

        self._caret_pos.end = pos
        return

    def _move_caret_by_word(self, direction: Literal["right", "left"]) -> None:
        start: int
        step: int
        match direction:
            case "right":
                start = self._caret_pos.end
                step = 1
            case "left":
                start = self._caret_pos.end - 1
                step = -1

        caret_pos = self._caret_pos.end
        entered_word = False
        for index, value in enumerate(self._value[start::step], 1):
            caret_pos = self._caret_pos.end + index * step

            if not entered_word:
                if value == " ":
                    continue
                else:
                    entered_word = True

            if value == " ":
                caret_pos -= step
                break

        self._set_caret_pos(caret_pos)
        return

    def _remove_selected_text(self) -> None:
        self._make_backup()

        start: int
        end: int
        if self._caret_pos.start <= self._caret_pos.end:
            start = self._caret_pos.start
            end = self._caret_pos.end
        else:
            start = self._caret_pos.end
            end = self._caret_pos.start

        self._value = self._value[:start] + self._value[end:]
        self._set_caret_pos(start)
        return

    def _remove_text(self) -> None:
        if self._caret_pos.end == 0:
            return

        self._make_backup()

        if self._value:
            self._value = (
                self._value[: self._caret_pos.end - 1]
                + self._value[self._caret_pos.end :]
            )
        self._set_caret_pos(self._caret_pos.end - 1)
        return

    def _input_text(self, text: str) -> None:
        self._make_backup()

        if self._caret_pos.has_selection():
            self._remove_selected_text()

        for character in text:
            candidate_text = (
                self._value[: self._caret_pos.end]
                + character
                + self._value[self._caret_pos.end :]
            )

            if self._pattern == "":
                self._value = candidate_text
                self._set_caret_pos(self._caret_pos.end + 1)
                continue

            # check pattern
            if re.fullmatch(self._pattern, candidate_text) is None:
                continue
            self._value = candidate_text
            self._set_caret_pos(self._caret_pos.end + 1)
        return

    def _make_backup(self) -> None:
        self._originator.text_state = self._value
        self._originator.caret_pos_state = self._caret_pos
        self._caretaker.make_backup()
        return

    def _undo(self) -> None:
        self._caretaker.undo()
        self._value = self._originator.text_state
        self._caret_pos = self._originator.caret_pos_state
        return
