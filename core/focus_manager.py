from __future__ import annotations

from typing import Optional

from core.canvas_item import CanvasItem


class FocusManager:
    """Manage about view focusing ( singleton )"""

    def __init__(self) -> None:
        self.__focused: Optional[CanvasItem] = None
        return

    def is_focused(self, view: CanvasItem) -> bool:
        return view is self.__focused

    def focus(self, view: CanvasItem) -> None:
        self.__focused = view
        return

    def unfocus(self, view: CanvasItem) -> None:
        if not self.is_focused(view):
            return

        self.__focused = None
        return


FOCUS_MANAGER = FocusManager()
