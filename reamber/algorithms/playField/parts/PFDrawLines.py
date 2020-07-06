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

    @staticmethod
    def colorTemplate(keys,
                      fromRgb: Tuple[int, int, int] = (79, 103, 255),
                      toRgb: Tuple[int, int, int] = (161, 255, 239),
                      furthest: float = 1000,
                      contrast:float = 1):
        """ Creates a quick lambda for color

        :param keys: Must be specified for this algorithm. Keys of the map. (m.notes.maxColumn() + 1)
        :param fromRgb Color when the column difference is the smallest
        :param toRgb: Color when the column difference is the largest
        :param furthest: The furthest distance before the scaling plateaus
        :param contrast: The contrast between differing offset differences. Exponential scaling.
        :return:
        """
        def func(col: int, offset: float):
            factor = 1 - (min(abs(offset), furthest) / furthest) ** (1 / contrast)
            newRgb = np.asarray(toRgb) + (np.asarray(fromRgb) - np.asarray(toRgb)) * (keys - (abs(col) + 1)) / keys
            newRgb = newRgb.astype(np.int)
            return *newRgb, int(255 * factor)
        return func

    @staticmethod
    def widthTemplate(keys,
                      fromWidth: int = 10,
                      toWidth: int = 1,
                      furthest: float = 1000,
                      contrast:float = 5):
        """ Creates a quick lambda for color

        :param keys: Must be specified for this algorithm. Keys of the map. (m.notes.maxColumn() + 1)
        :param fromWidth: Width when the column difference is the smallest
        :param toWidth: Width when the column difference is the largest
        :param furthest: The furthest distance before the scaling plateaus
        :param contrast: The contrast between differing offset differences. Exponential scaling.
        :return:
        """
        def func(col: int, offset: float):
            factor = 1 - (min(abs(offset), furthest) / furthest) ** (1 / contrast)
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