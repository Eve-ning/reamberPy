from __future__ import annotations

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable


class PFDrawColumnLines(PFDrawable):

    def __init__(self,
                 color: str = "#2b2b2b"):
        """Draws column lines, separating columns of notes"""
        self.color = color

    def draw(self, pf: PlayField) -> PlayField:
        """Refer to __init__"""

        # Fencepost, if key = 4, we draw on 1 2 3
        for col_line in range(1, int(pf.keys)):
            for w in range(pf.column_line_width):
                pf.canvas_draw.line([
                    pf.get_pos(
                        pf.m.stack().offset.max(), col_line, x_offset=w - 1
                    ),
                    pf.get_pos(0, col_line, x_offset=w - 1)],
                    fill=self.color)
        return pf
