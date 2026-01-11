from __future__ import annotations

from core.interact.keyboard import KeyboardInteractable
from core.interact.mouse import MouseInteractable
from core.view import View


class ContainerView(View, MouseInteractable, KeyboardInteractable):
    def __init__(self) -> None:
        super().__init__()
        self._init_mouse_interaction()
        self._init_keyboard_interaction()
