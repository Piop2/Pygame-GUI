from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto

from model.vector import Vector


class InputEvent(ABC):
    pass


class MouseButton(Enum):
    LEFT = auto()
    WHEEL = auto()
    RIGHT = auto()


@dataclass(frozen=True)
class MouseDownEvent(InputEvent):
    key: MouseButton
    position: Vector


@dataclass(frozen=True)
class MouseUpEvent(InputEvent):
    key: MouseButton
    position: Vector


@dataclass(frozen=True)
class MouseScrollUpEvent(InputEvent):
    position: Vector


@dataclass(frozen=True)
class MouseScrollEvent(InputEvent):
    delta: Vector
    position: Vector


@dataclass(frozen=True)
class KeyDownEvent(InputEvent):
    key: int


@dataclass(frozen=True)
class KeyUpEvent(InputEvent):
    key: int


@dataclass(frozen=True)
class KeyInputEvent(InputEvent):
    text: str
