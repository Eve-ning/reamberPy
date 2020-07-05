from __future__ import annotations
from PIL import Image, ImageDraw

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
                 color:Callable[[int, float], str or Tuple] = lambda x,y: "#999999"):
        """ The draws listed lines on the field

        :param lines: The lines to draw
        """
        self.lines = lines
        self.color = color

    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """

        for line in self.lines:
            pf.canvasDraw.line([pf.getPos(column=line.colFrom, offset=line.offsetFrom,
                                          xoffset=pf.noteWidth/2, yoffset=-pf.hitHeight/2),
                                pf.getPos(column=line.colTo, offset=line.offsetTo,
                                          xoffset=pf.noteWidth/2, yoffset=-pf.hitHeight/2)],
                               fill=self.color(line.colTo - line.colFrom, line.offsetTo - line.offsetFrom),
                               width=4)

        return pf
