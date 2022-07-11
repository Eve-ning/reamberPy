from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Callable

import numpy as np

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable


@dataclass
class PFLine:
    """A dataclass holding the coordinates for PFDrawLines Generation"""
    col_from: int
    col_to: int
    offset_from: float
    offset_to: float


class PFDrawLines(PFDrawable):

    def __init__(self,
                 lines: List[PFLine],
                 color: Callable[[int, float], str | Tuple] =
                 lambda x, y: "#999999",
                 width: Callable[[int, float], int] = lambda x, y: 1):
        """The draws listed lines on the field

        Args:
            lines: The lines to draw
            color: The lambda to determine color.
                func(colDifference, offsetDifference) -> str or rgba Tuple
            width: The lambda to determine width.
                func(colDifference, offsetDifference) -> int
        """
        self.lines = lines
        self.color = color
        self.width = width

    class Colors:
        BLUE = {"from_rgb": (79, 103, 255), "to_rgb": (161, 255, 239)}
        ORANGE = {"from_rgb": (255, 167, 43), "to_rgb": (255, 197, 115)}
        GREEN = {"from_rgb": (15, 255, 47), "to_rgb": (133, 255, 149)}
        PINK = {"from_rgb": (247, 64, 202), "to_rgb": (255, 130, 224)}
        RED = {"from_rgb": (255, 28, 28), "to_rgb": (255, 148, 148)}
        PURPLE = {"from_rgb": (177, 51, 255), "to_rgb": (220, 163, 255)}

    @staticmethod
    def color_lambda(
        keys,
        from_rgb: Tuple[int, int, int] = (79, 103, 255),
        to_rgb: Tuple[int, int, int] = (161, 255, 239),
        nearest: float = 100,
        furthest: float = 1000
    ) -> Callable[[int, float], Tuple[int, int, int, int]]:
        """Creates a quick lambda for color

        This can be used in PFDrawLines(color=PFDrawLines.color_lambda(...))

        Args:
            keys: Keys of the map
            from_rgb: Color when the column difference is the smallest
            to_rgb: Color when the column difference is the largest
            nearest: The largest distance where the color is from_rgb
            furthest: The smallest distance where the color is to_rgb

        Returns:
             Callable used by DrawLines and returns a RGBA Tuple
        """

        def func(col: int, offset: float) -> Tuple[int, int, int, int]:
            clamp = max(nearest, min(furthest, abs(offset)))
            offset_factor = 1 - (clamp - nearest) / (furthest - nearest)
            col_factor = 1 - abs(col) / (keys - 1)
            new_rgb = np.asarray(to_rgb) + \
                      (np.asarray(from_rgb) - np.asarray(to_rgb)) * \
                      offset_factor * col_factor
            new_rgb = (*new_rgb.astype(int),
                       int(255 * offset_factor * col_factor))
            # noinspection PyTypeChecker
            return new_rgb

        return func

    @staticmethod
    def width_lambda(keys,
                     from_width: int = 5,
                     to_width: int = 1,
                     nearest: float = 100,
                     furthest: float = 1000) -> Callable[[int, float], int]:
        """Creates a quick lambda for color

        This can be used in PFDrawLines(color=PFDrawLines.width_lambda(...))

        Returns the expected width

        Args:
            keys: Keys of the map. (m.notes.maxColumn() + 1)
            from_width: Width when the column difference is the smallest
            to_width: Width when the column difference is the largest
            nearest: The largest distance where the color is from_rgb
            furthest: The smallest distance where the color is to_rgb
        """

        def func(col: int, offset: float) -> int:
            clamp = max(nearest, min(furthest, abs(offset)))
            offset_factor = 1 - (clamp - nearest) / (furthest - nearest)
            col_factor = 1 - abs(col) / (keys - 1)
            return int(to_width + (
                from_width - to_width) * offset_factor * col_factor)

        return func

    def draw(self, pf: PlayField) -> PlayField:
        """Refer to __init__"""

        for line in self.lines:
            pf.canvas_draw.line(
                [
                    pf.get_pos(
                        column=line.col_from,
                        offset=line.offset_from,
                        x_offset=pf.note_width / 2,
                        y_offset=-pf.hit_height / 2),
                    pf.get_pos(
                        column=line.col_to,
                        offset=line.offset_to,
                        x_offset=pf.note_width / 2,
                        y_offset=-pf.hit_height / 2)
                ],
                fill=self.color(line.col_to - line.col_from,
                                line.offset_to - line.offset_from),
                width=self.width(line.col_to - line.col_from,
                                 line.offset_to - line.offset_from)
            )

        return pf

    @staticmethod
    def from_combo(combo: np.ndarray,
                   keys: int,
                   from_rgb: Tuple[int, int, int],
                   to_rgb: Tuple[int, int, int],
                   from_width=5,
                   to_width=1,
                   nearest: float = 50,
                   furthest: float = 300) -> PFDrawLines:
        """Draw combination lines on the PF

        Args:
            combo:
            keys: The keys of the map, used to detect pattern limits.
            from_rgb: Color when the column/offset difference is the smallest
            to_rgb: Color when the column/offset difference is the largest
            from_width: Width when the column difference is the smallest
            to_width: Width when the column difference is the largest
            nearest: The largest distance where the color is from_rgb
            furthest: The smallest distance where the color is to_rgb
        """

        return PFDrawLines(
            [*[PFLine(i['column'][0], i['column'][1],
                      i['offset'][0], i['offset'][1])
               for i in combo]],
            color=PFDrawLines.color_lambda(keys,
                                           from_rgb=from_rgb,
                                           to_rgb=to_rgb,
                                           nearest=nearest,
                                           furthest=furthest),
            width=PFDrawLines.width_lambda(keys,
                                           from_width=from_width,
                                           to_width=to_width,
                                           nearest=nearest,
                                           furthest=furthest))
