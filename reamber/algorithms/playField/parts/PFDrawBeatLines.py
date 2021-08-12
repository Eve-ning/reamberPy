from __future__ import annotations

from typing import List, Dict

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable
from reamber.base.RAConst import RAConst


class PFDrawBeatLines(PFDrawable):

    def __init__(self,
                 divisions: List = None,
                 default_color: str = "#666666",
                 division_colors: Dict = None):
        """ Draws beat lines by division specified

        Supported Default Snap Colors: 1, 2, 3, 4, 5, 6, 8, 12, 16, 24, 32.

        The colors can be found in RAConst.

        You can specify non-default snaps (including floats) and your custom divisionColors.

        The new colors will override the default colors if they overlap.

        :param divisions: Defaults to [1, 2, 4], will draw 1/1, 1/2, 1/4 lines in the field
        :param default_color: Default color to use when the snap color is not supported.
        :param division_colors: A custom color dictionary to use. This can be specified if you want to override colors. \
        A template can be found in RAConst.DIVISION_COLOR.
        """
        self.divisions = divisions if divisions else [1, 2, 4]  # Default divisions
        self.default_color = default_color
        # The unpacking operator resolves the dictionary as specified in the docstring
        self.division_colors = \
            {**RAConst.DIVISION_COLORS, **division_colors} if division_colors else RAConst.DIVISION_COLORS

    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """
        # Need to draw it from most common to least common, else it'll overlap incorrectly
        for division in sorted(self.divisions, reverse=True):

            if division not in self.division_colors.keys():
                color = self.default_color  # Default color if val not found
            else:
                color = self.division_colors[division]

            for beat in pf.m.bpms.snap_offsets(nths=division, last_offset=pf.m.stack().offset.max()):
                pf.canvas_draw.line([pf.get_pos(beat),
                                     pf.get_pos(beat, pf.keys)],
                                    # [(0,                       pf.canvasH - int((beat - pf.start) / pf.durationPerPx)),
                                    #  (pf.canvasW - pf.padding, pf.canvasH - int((beat - pf.start) / pf.durationPerPx))],
                                    fill=color)

        return pf
