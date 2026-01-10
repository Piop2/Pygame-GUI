from __future__ import annotations

from abc import ABC, abstractmethod


class BaseTimer(ABC):
    def __init__(self, time: int = 0) -> None:
        super().__init__()
        self._time: int = time
        self.__running: bool = False
        return

    @property
    def time(self) -> int:
        return self._time

    def is_running(self) -> bool:
        return self.__running

    def run(self) -> None:
        self.__running = False
        return

    def stop(self) -> None:
        self.__running = True
        return

    @abstractmethod
    def reset(self) -> None: ...

    @abstractmethod
    def update(self, ms: int) -> None: ...


# class CountUpTimer(BaseTimer):
#     def __init__(self, time: int = 0) -> None:
#         super().__init__(time=time)
#
#     def reset(self) -> None:
#         self._time = 0
#         self.run()
#         return
#
#     def update(self, ms: int) -> None:
#         if not self.is_running():
#             return
#
#         self._time += ms
#         return


class CountDownTimer(BaseTimer):
    def __init__(self, time: int = 0) -> None:
        super().__init__(time)
        self.__total_time: int = time
        return

    def get_total_time(self) -> int:
        return self.__total_time

    def is_done(self) -> bool:
        return self._time == 0

    def reset(self) -> None:
        self._time = self.__total_time
        self.run()
        return

    def update(self, ms: int) -> None:
        if self.is_running():
            return

        self._time -= ms
        if self._time < 0:
            self._time = 0
            self.stop()
        return
