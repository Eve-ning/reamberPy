from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Callable

import numpy as np

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable


@dataclass
class PFLine:
    """ A dataclass holding the coordinates for PFDrawLines Generation"""
    col_from: int
    col_to: int
    offset_from: float
    offset_to: float

class PFDrawLines(PFDrawable):

    def __init__(self,
                 lines: List[PFLine],
                 color: Callable[[int, float], str or Tuple] = lambda x,y: "#999999",
                 width: Callable[[int, float], int] = lambda x,y: 1):
        """ The draws listed lines on the field

        :param lines: The lines to draw
        :param color: The lambda to determine color. func(colDifference, offsetDifference) -> str or rgba Tuple
        :param width: The lambda to determine width. func(colDifference, offsetDifference) -> int
        """
        self.lines = lines
        self.color = color
        self.width = width

    class Colors:
        BLUE   = {"from_rgb": (79, 103, 255), "to_rgb": (161, 255, 239)}
        ORANGE = {"from_rgb": (255, 167, 43), "to_rgb": (255, 197, 115)}
        GREEN  = {"from_rgb": (15, 255, 47),  "to_rgb": (133, 255, 149)}
        PINK   = {"from_rgb": (247, 64, 202), "to_rgb": (255, 130, 224)}
        RED    = {"from_rgb": (255, 28, 28),  "to_rgb": (255, 148, 148)}
        PURPLE = {"from_rgb": (177, 51, 255), "to_rgb": (220, 163, 255)}

    @staticmethod
    def color_template(keys,
                       from_rgb: Tuple[int, int, int] = (79, 103, 255),
                       to_rgb: Tuple[int, int, int] = (161, 255, 239),
                       nearest: float = 100,
                       furthest: float = 1000):
        """ Creates a quick lambda for color

        :param keys: Must be specified for this algorithm. Keys of the map. (m.notes.maxColumn() + 1)
        :param from_rgb: Color when the column difference is the smallest
        :param to_rgb: Color when the column difference is the largest
        :param nearest: The largest distance where the color is from_rgb
        :param furthest: The smallest distance where the color is to_rgb
        :return:
        """

        def func(col: int, offset: float):
            clamp = max(nearest, min(furthest, abs(offset)))
            offset_factor = 1 - (clamp - nearest) / (furthest - nearest)
            col_factor = 1 - abs(col) / (keys - 1)
            new_rgb = np.asarray(to_rgb) + (np.asarray(from_rgb) - np.asarray(to_rgb)) * offset_factor * col_factor
            new_rgb = new_rgb.astype(np.int)
            return *new_rgb, int(255 * offset_factor * col_factor)
        return func

    @staticmethod
    def width_template(keys,
                       from_width: int = 5,
                       to_width: int = 1,
                       nearest: float = 100,
                       furthest: float = 1000):
        """ Creates a quick lambda for color

        :param keys: Must be specified for this algorithm. Keys of the map. (m.notes.maxColumn() + 1)
        :param from_width: Width when the column difference is the smallest
        :param to_width: Width when the column difference is the largest
        :param nearest: The largest distance where the color is from_rgb
        :param furthest: The smallest distance where the color is to_rgb
        :return:
        """
        def func(col: int, offset: float):
            clamp = max(nearest, min(furthest, abs(offset)))
            offset_factor = 1 - (clamp - nearest) / (furthest - nearest)
            col_factor = 1 - abs(col) / (keys - 1)
            return int(to_width + (from_width - to_width) * offset_factor * col_factor)
        return func

    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """

        for line in self.lines:
            pf.canvas_draw.line([pf.get_pos(column=line.col_from, offset=line.offset_from,
                                            x_offset=pf.note_width / 2, y_offset=-pf.hit_height / 2),
                                 pf.get_pos(column=line.col_to, offset=line.offset_to,
                                            x_offset=pf.note_width / 2, y_offset=-pf.hit_height / 2)],
                                fill=self.color(line.col_to - line.col_from, line.offset_to - line.offset_from),
                                width=self.width(line.col_to - line.col_from, line.offset_to - line.offset_from))

        return pf

    @staticmethod
    def fromCombo(combo: np.ndarray,
                  keys:int,
                  from_rgb: Tuple[int, int, int],
                  to_rgb: Tuple[int, int, int],
                  from_width=5,
                  to_width=1,
                  nearest: float = 50,
                  furthest: float = 300) -> PFDrawLines:
        """ A template to quickly create jack lines

        E.g. If the ``minimumLength==2``, all jacks that last at least 2 notes are highlighted.

        :param combo:
        :param keys: The keys of the map, used to detect pattern limits.
        :param from_rgb: Color when the column/offset difference is the smallest
        :param to_rgb: Color when the column/offset difference is the largest
        :param from_width: Width when the column difference is the smallest
        :param to_width: Width when the column difference is the largest
        :param nearest: The largest distance/difference where the color is from_rgb
        :param furthest: The smallest distance/difference where the color is to_rgb
        :return:
        """

        return PFDrawLines([*[PFLine(i['column0'], i['column1'], i['offset0'], i['offset1']) for i in combo]],
                           color=PFDrawLines.color_template(keys,
                                                            from_rgb=from_rgb, to_rgb=to_rgb,
                                                            nearest=nearest, furthest=furthest),
                           width=PFDrawLines.width_template(keys,
                                                            from_width=from_width, to_width=to_width,
                                                            nearest=nearest, furthest=furthest))
