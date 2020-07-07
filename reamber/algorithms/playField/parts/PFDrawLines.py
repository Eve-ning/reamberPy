from __future__ import annotations
import numpy as np

from reamber.algorithms.playField.parts.PFDrawable import PFDrawable
from reamber.algorithms.playField import PlayField

from typing import List, Tuple, Callable
from dataclasses import dataclass

@dataclass
class PFLine:
    colFrom: int
    colTo: int
    offsetFrom: float
    offsetTo: float

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

    COLOR_BLUE      = {"fromRgb": (79, 103, 255), "toRgb": (161, 255, 239)}
    COLOR_ORANGE    = {"fromRgb": (255, 167, 43), "toRgb": (255, 197, 115)}
    COLOR_GREEN     = {"fromRgb": (15, 255, 47),  "toRgb": (133, 255, 149)}
    COLOR_PINK      = {"fromRgb": (247, 64, 202), "toRgb": (255, 130, 224)}
    COLOR_RED       = {"fromRgb": (255, 28, 28),  "toRgb": (255, 148, 148)}
    COLOR_PURPLE    = {"fromRgb": (177, 51, 255), "toRgb": (220, 163, 255)}

    @staticmethod
    def colorTemplate(keys,
                      fromRgb: Tuple[int, int, int] = (79, 103, 255),
                      toRgb: Tuple[int, int, int] = (161, 255, 239),
                      nearest: float = 100,
                      furthest: float = 1000,
                      contrast: float = 1):
        """ Creates a quick lambda for color

        :param keys: Must be specified for this algorithm. Keys of the map. (m.notes.maxColumn() + 1)
        :param fromRgb Color when the column difference is the smallest
        :param toRgb: Color when the column difference is the largest
        :param nearest: The largest distance where the color is fromRgb
        :param furthest: The smallest distance where the color is toRgb
        :param contrast: The contrast between differing offset differences.
        :return:
        """

        def func(col: int, offset: float):
            clamp = max(nearest, min(furthest, abs(offset)))
            factor = 1 - (((clamp - nearest) / (furthest - nearest) + 0.5) * contrast - 0.5)
            newRgb = np.asarray(toRgb) + (np.asarray(fromRgb) - np.asarray(toRgb)) * (keys - (abs(col) + 1)) / keys
            newRgb = newRgb.astype(np.int)
            return *newRgb, int(255 * factor)
        return func

    @staticmethod
    def widthTemplate(keys,
                      fromWidth: int = 10,
                      toWidth: int = 1,
                      nearest: float = 100,
                      furthest: float = 1000,
                      contrast:float = 5):
        """ Creates a quick lambda for color

        :param keys: Must be specified for this algorithm. Keys of the map. (m.notes.maxColumn() + 1)
        :param fromWidth: Width when the column difference is the smallest
        :param toWidth: Width when the column difference is the largest
        :param nearest: The largest distance where the color is fromRgb
        :param furthest: The smallest distance where the color is toRgb
        :param contrast: The contrast between differing offset differences.
        :return:
        """
        def func(col: int, offset: float):
            clamp = max(nearest, min(furthest, abs(offset)))
            factor = 1 - (((clamp - nearest) / (furthest - nearest) + 0.5) * contrast - 0.5)
            newWidth = toWidth + (fromWidth - toWidth) * (keys - (abs(col) + 1)) / keys
            return int(newWidth * factor)
        return func

    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """

        for line in self.lines:
            pf.canvasDraw.line([pf.getPos(column=line.colFrom, offset=line.offsetFrom,
                                          xoffset=pf.noteWidth/2, yoffset=-pf.hitHeight/2),
                                pf.getPos(column=line.colTo, offset=line.offsetTo,
                                          xoffset=pf.noteWidth/2, yoffset=-pf.hitHeight/2)],
                               fill=self.color(line.colTo - line.colFrom, line.offsetTo - line.offsetFrom),
                               width=self.width(line.colTo - line.colFrom, line.offsetTo - line.offsetFrom))

        return pf

    def templateChordStream(self):
        """ Generates a color and width lambda to detect chordStreams.

        Unpack as ** to retrieve lambdas."""
        pass