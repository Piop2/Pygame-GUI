from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import IntEnum

from pygame.math import Vector2


class MouseButton(IntEnum):
    LEFT = 1
    WHEEL = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


class InputEvent(ABC):
    pass


class MouseEvent(InputEvent):
    pass


class KeyEvent(InputEvent):
    pass


@dataclass(frozen=True)
class MouseDownEvent(MouseEvent):
    key: int
    pos: Vector2


@dataclass(frozen=True)
class MouseUpEvent(MouseEvent):
    key: int
    pos: Vector2


@dataclass(frozen=True)
class MouseMotionEvent(MouseEvent):
    pos: Vector2


@dataclass(frozen=True)
class MouseScrollEvent(MouseEvent):
    delta: Vector2


@dataclass(frozen=True)
class MouseEnterEvent(MouseEvent):
    pass


@dataclass(frozen=True)
class MouseExitEvent(MouseEvent):
    pass


@dataclass(frozen=True)
class KeyDownEvent(KeyEvent):
    key: int


@dataclass(frozen=True)
class KeyUpEvent(KeyEvent):
    key: int


@dataclass(frozen=True)
class TextInputEvent(KeyEvent):
    text: str
