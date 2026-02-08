from __future__ import annotations

from view.input_box.memento.originator import Originator
from view.input_box.memento.snapshot import Snapshot
from view.text.caret import CaretPos


class Caretaker:
    def __init__(self, originator: Originator) -> None:
        self._originator = originator
        self._history: list[Snapshot[tuple[str, CaretPos]]] = []
        return

    def make_backup(self) -> None:
        self._history.append(self._originator.create_snapshot())
        return

    def undo(self) -> None:
        try:
            backup = self._history.pop()
            self._originator.restore(backup)

            if not self._history:
                self.make_backup()
        except IndexError:
            pass
        return
