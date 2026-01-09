from __future__ import annotations

from enum import Enum, auto


class ContentAlign(Enum):
    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()

    MIDDLE_LEFT = auto()
    MIDDLE_CENTER = auto()
    MIDDLE_RIGHT = auto()

    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()


def calc_aligned_pos(
    content_align: ContentAlign,
    container_size: tuple[int, int],
    content_size: tuple[int, int],
) -> tuple[int, int]:
    x = 0
    match content_align:
        case (
            ContentAlign.TOP_LEFT | ContentAlign.MIDDLE_LEFT | ContentAlign.BOTTOM_LEFT
        ):
            pass
        case (
            ContentAlign.TOP_RIGHT
            | ContentAlign.MIDDLE_RIGHT
            | ContentAlign.BOTTOM_RIGHT
        ):
            x = container_size[0] - content_size[0]
        case (
            ContentAlign.TOP_CENTER
            | ContentAlign.MIDDLE_CENTER
            | ContentAlign.BOTTOM_CENTER
        ):
            x = (container_size[0] // 2) - (content_size[0] // 2)

    y = 0
    match content_align:
        case ContentAlign.TOP_LEFT | ContentAlign.TOP_CENTER | ContentAlign.TOP_RIGHT:
            y = 0
        case (
            ContentAlign.MIDDLE_LEFT
            | ContentAlign.MIDDLE_CENTER
            | ContentAlign.MIDDLE_RIGHT
        ):
            y = (container_size[1] // 2) - (content_size[1] // 2)
        case (
            ContentAlign.BOTTOM_LEFT
            | ContentAlign.BOTTOM_CENTER
            | ContentAlign.BOTTOM_RIGHT
        ):
            y = container_size[1] - content_size[1]

    return x, y


# class TextAlign(Enum): ...
