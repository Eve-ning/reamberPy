from reamber.algorithms.analysis.playField import PlayField
from reamber.algorithms.analysis.playField.parts.PFDrawable import PFDrawable
from reamber.algorithms.analysis.bpm.bpmBeatOffsets import bpmBeatOffsets

from reamber.base.RAConst import RAConst

from typing import List, Dict


class PFDrawBeatLines(PFDrawable):

    def __init__(self,
                 divisions: List = None,
                 defaultColor: str = "#666666",
                 divisionColors: Dict = None):
        """ Draws beat lines by division specified
        :param divisions: e.g. [1, 2, 4] will draw 1/1, 1/2, 1/4 lines in the field
        :param defaultColor: Default color to use when the snap color is not supported.
        Supported Snap Colors: 1, 2, 3, 4, 6, 8, 12, 16, 24, 32
        The colors can be found in RAConst
        :param divisionColors: A custom color dictionary to use. This can be specified if you want to override colors.
        A template can be found in RAConst.DIVISION_COLOR.
        """
        self.divisions = divisions if divisions else [1, 2, 4]  # Default divisions
        self.defaultColor = defaultColor
        self.divisionColors = divisionColors if divisionColors else RAConst.DIVISION_COLORS

    def draw(self, pf: PlayField) -> PlayField:
        """[DRAW BEAT LINES]"""
        # Need to draw it from most common to least common, else it'll overlap incorrectly
        for division in sorted(self.divisions, reverse=True):

            if division not in self.divisionColors.keys():
                color = self.defaultColor  # Default color if val not found
            else:
                color = self.divisionColors[division]

            for beat in bpmBeatOffsets(pf.m.bpms, nths=division, lastOffset=pf.m.notes.lastOffset()):
                pf.canvasDraw.line(
                    [(0,                       pf.canvasH - int((beat - pf.start) / pf.durationPerPx)),
                     (pf.canvasW - pf.padding, pf.canvasH - int((beat - pf.start) / pf.durationPerPx))],
                    fill=color)

        return pf
