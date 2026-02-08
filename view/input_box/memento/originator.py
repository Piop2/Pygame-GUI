from __future__ import annotations

from copy import deepcopy

from view.text.caret import CaretPos
from view.input_box.memento.snapshot import Snapshot


class Originator:
    def __init__(self) -> None:
        self.text_state: str = ""
        self.caret_pos_state: CaretPos = CaretPos(0, 0)
        return

    def create_snapshot(self) -> Snapshot[tuple[str, CaretPos]]:
        return Snapshot((self.text_state, deepcopy(self.caret_pos_state)))

    def restore(self, memento: Snapshot[tuple[str, CaretPos]]) -> None:
        self.text_state = memento.state[0]
        self.caret_pos_state = memento.state[1]
        return
