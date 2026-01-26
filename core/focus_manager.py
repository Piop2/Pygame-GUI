from __future__ import annotations

from typing import Optional

from core.view import View


class FocusManager:
    """Manage about view focusing ( singleton )"""

    def __init__(self) -> None:
        self.__focused: Optional[View] = None

    def is_focused(self, view: View) -> bool:
        return view is self.__focused

    def focus(self, view: View) -> None:
        self.__focused = view

    def unfocus(self, view: View) -> None:
        if not self.is_focused(view):
            return

        self.__focused = None


FOCUS_MANAGER = FocusManager()
