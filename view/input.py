from __future__ import annotations

from core.view import View
from core.protocol.has_value import HasValue
from view.text import TextView


"""Input View 구현 방안...
- 아마도 child에 Text View를 무조건 두어야 함..

- 1안) Text View를 상속받아서 Input View로 만드는 것도 방법..
- 2안) 그냥 Input View에 child 추가를 못 하게 막고, Text View만 쓰게 하는 방법
"""


# 2안으로 진행중
class InputView(View, HasValue[str]):
    def __init__(self) -> None:
        super().__init__()

        self._text_view = TextView()

        self._children = [self._text_view]

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

    def update(self, delta: int) -> None:
        self._text_view.style.size = self.style.size
