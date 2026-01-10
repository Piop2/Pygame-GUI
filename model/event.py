from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, Enum, auto


@dataclass
class UIEvent: ...


class MouseButton(IntEnum):
    NONE = 0
    LEFT = 1
    WHEEL = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


@dataclass
class MouseEvent(UIEvent):
    key: MouseButton
    x: int
    y: int


@dataclass
class MouseDownEvent(MouseEvent): ...


@dataclass
class MouseUpEvent(MouseEvent): ...


class KeyboardEventType(Enum):
    DOWN = auto()
    UP = auto()
    INPUT = auto()


@dataclass
class KeyboardEvent(UIEvent):
    type: KeyboardEventType
    key: int
    text: str
