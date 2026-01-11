from __future__ import annotations

from typing import Protocol, runtime_checkable

from model.style import Style


@runtime_checkable
class Styled(Protocol):
    _style: Style

    @property
    def style(self) -> Style:
        return self._style

    @style.setter
    def style(self, new: Style) -> None:
        self._style = new
