from __future__ import annotations

from typing import List, Dict

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable
from reamber.base.RAConst import RAConst


class PFDrawBeatLines(PFDrawable):

    def __init__(self,
                 divisions: List = (1, 2, 4),
                 default_color: str = "#666666",
                 division_colors: Dict = None):
        """Draws beat lines by division specified

        Supported Default Snap Colors: 1, 2, 3, 4, 5, 6, 8, 12, 16, 24, 32.

        The colors can be found in RAConst.

        You can specify non-default snaps (including floats) and your custom
        division_colors.

        The new colors will override the default colors if they overlap.

        Args:
            divisions: Draws the 1/n lines in the field
            default_color: Default color for unsupported snap colors
            division_colors: A custom color dictionary to use.
                A template can be found in RAConst.DIVISION_COLORS.
        """
        self.divisions = divisions
        self.default_color = default_color
        self.division_colors = {**RAConst.DIVISION_COLORS, **division_colors} \
            if division_colors else RAConst.DIVISION_COLORS

    def draw(self, pf: PlayField) -> PlayField:
        """Refer to __init__"""

        # Draw it from most to least common, else it'll overlap incorrectly
        for division in sorted(self.divisions, reverse=True):

            color = self.division_colors.get(division, self.default_color)
            for beat in pf.m.bpms.snap_offsets(
                nths=division,
                last_offset=pf.m.stack().offset.max()
            ):
                pf.canvas_draw.line([
                    pf.get_pos(beat),
                    pf.get_pos(beat, pf.keys)
                ],
                    fill=color)

        return pf
