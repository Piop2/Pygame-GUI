from __future__ import annotations

from typing import Callable, Optional, Literal
from enum import Enum

from pgui.util.timer import CountDownTimer


class DelayedHandler[T: Enum]:
    def __init__(self, handler: Callable[[], T], delay: int) -> None:
        self._timer = CountDownTimer(delay)
        self._handler = handler
        return

    def __call__(self, delta: int) -> Optional[T]:
        self._timer.update(delta)

        next_action: Optional[T] = None
        if self._timer.is_done():
            next_action = self._handler()

        return next_action

    def reset(self) -> None:
        self._timer.reset()
        return


class Action[T: Enum]:
    def __init__(self) -> None:
        self._current_action: Optional[T] = None
        self._current_event: Literal["press", "release"] = "release"

        self.action_handlers: dict[
            Literal["press", "release"], dict[T, DelayedHandler]
        ] = {"press": {}, "release": {}}
        return

    def register_handler(
        self,
        event: Literal["press", "release"],
        action: T | tuple[T, ...],
        delay: int = 0,
    ) -> Callable[[Callable[[], T]], None]:
        if not isinstance(action, tuple):
            action = (action,)

        def decorator(handler: Callable[[], T]) -> None:
            for action_type in action:
                self.action_handlers[event][action_type] = DelayedHandler(
                    handler, delay
                )
            return

        return decorator

    def _get_last_handler(self) -> Optional[DelayedHandler]:
        return self.action_handlers[self._current_event].get(self._current_action)

    def set_action(self, action: Optional[T]):
        handler = self._get_last_handler()
        if handler is not None:
            handler.reset()

        self._current_action = action
        return

    def reset(self) -> None:
        self._current_action = None
        self._current_event = "release"

        for handler_dict in self.action_handlers.values():
            for handler in handler_dict.values():
                handler.reset()
        return

    def press(self) -> None:
        if (
            self._current_event != "press"
            and (handler := self._get_last_handler()) is not None
        ):
            handler.reset()

        self._current_event = "press"
        return

    def release(self) -> None:
        if (
            self._current_event != "release"
            and (handler := self._get_last_handler()) is not None
        ):
            handler.reset()

        self._current_event = "release"
        return

    def update(self, delta: int) -> None:
        if self._current_action is None:
            return

        handler = self.action_handlers[self._current_event].get(self._current_action)
        if handler is None:
            return

        next_action = handler(delta)
        if next_action is not None:
            self.set_action(next_action)
        return
