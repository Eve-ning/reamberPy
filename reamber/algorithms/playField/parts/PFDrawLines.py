from __future__ import annotations
import numpy as np

from reamber.algorithms.playField.parts.PFDrawable import PFDrawable
from reamber.algorithms.playField import PlayField
from reamber.base.Hold import Hold, HoldTail
from reamber.base.Hit import Hit


from typing import List, Tuple, Callable
from dataclasses import dataclass
from reamber.base.Map import Map

from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterCombo, PtnFilterChord, PtnFilterType

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

    class Colors:
        BLUE   = {"fromRgb": (79, 103, 255), "toRgb": (161, 255, 239)}
        ORANGE = {"fromRgb": (255, 167, 43), "toRgb": (255, 197, 115)}
        GREEN  = {"fromRgb": (15, 255, 47),  "toRgb": (133, 255, 149)}
        PINK   = {"fromRgb": (247, 64, 202), "toRgb": (255, 130, 224)}
        RED    = {"fromRgb": (255, 28, 28),  "toRgb": (255, 148, 148)}
        PURPLE = {"fromRgb": (177, 51, 255), "toRgb": (220, 163, 255)}

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
            offsetFactor = 1 - (clamp - nearest) / (furthest - nearest)
            colFactor = 1 - abs(col) / (keys - 1)
            newRgb = np.asarray(toRgb) + (np.asarray(fromRgb) - np.asarray(toRgb)) * offsetFactor * colFactor
            newRgb = newRgb.astype(np.int)
            return *newRgb, int(255 * offsetFactor * colFactor)
        return func

    @staticmethod
    def widthTemplate(keys,
                      fromWidth: int = 5,
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
            offsetFactor = 1 - (clamp - nearest) / (furthest - nearest)
            colFactor = 1 - abs(col) / (keys - 1)
            return int(toWidth + (fromWidth - toWidth) * offsetFactor * colFactor)
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

    @staticmethod
    def templateChordStream(primary:int, secondary:int,
                            keys:int, groups: List[np.ndarray],
                            fromRgb: Tuple[int, int, int],
                            toRgb: Tuple[int, int, int],
                            contrast: float = 0.7,
                            nearest: float = 100,
                            furthest: float = 1000,
                            fromWidth=5) -> PFDrawLines:
        """ A template to quickly create chordstream lines """

        combo = Pattern.combinations(
            groups,
            size=2,
            flatten=True,
            makeSize2=True,
            chordFilter=PtnFilterChord.create(
                [[primary, secondary]], keys=keys,
                method=PtnFilterChord.Method.ANY_ORDER | PtnFilterChord.Method.AND_LOWER,
                invertFilter=False).filter,
            comboFilter=PtnFilterCombo.create(
                [[0, 0]], keys=keys,
                method=PtnFilterCombo.Method.REPEAT,
                invertFilter=True).filter,
            typeFilter=PtnFilterType.create(
                [[HoldTail, object]],
                method=PtnFilterType.Method.ANY_ORDER,
                invertFilter=True).filter)

        return PFDrawLines([*[PFLine(i['column0'], i['column1'], i['offset0'], i['offset1']) for i in combo]],
                    color=PFDrawLines.colorTemplate(keys,
                                                    fromRgb=fromRgb, toRgb=toRgb, contrast=contrast,
                                                    nearest=nearest,furthest=furthest),
                    width=PFDrawLines.widthTemplate(keys, fromWidth=fromWidth,
                                                    nearest=nearest,furthest=furthest))

    @staticmethod
    def templateJacks(minimumLength: int,
                      keys:int, groups: List[np.ndarray],
                      fromRgb: Tuple[int, int, int],
                      toRgb: Tuple[int, int, int],
                      nearest: float = 50,
                      furthest: float = 300,
                      fromWidth=5) -> PFDrawLines:
        """ A template to quickly create chordstream lines """

        assert minimumLength >= 2, f"Minimum Length must be at least 2, {minimumLength} < 2"
        combo = Pattern.combinations(
            groups,
            size=minimumLength,
            flatten=True,
            makeSize2=True,
            comboFilter=PtnFilterCombo.create(
                [[0] * minimumLength], keys=keys,
                method=PtnFilterCombo.Method.REPEAT,
                invertFilter=False).filter,
            typeFilter=PtnFilterType.create(
                [[HoldTail, object]],
                method=PtnFilterType.Method.ANY_ORDER,
                invertFilter=True).filter)

        return PFDrawLines([*[PFLine(i['column0'], i['column1'], i['offset0'], i['offset1']) for i in combo]],
                    color=PFDrawLines.colorTemplate(keys, fromRgb=fromRgb, toRgb=toRgb, nearest=nearest, furthest=furthest),
                    width=PFDrawLines.widthTemplate(keys, fromWidth=fromWidth, nearest=nearest, furthest=furthest))
