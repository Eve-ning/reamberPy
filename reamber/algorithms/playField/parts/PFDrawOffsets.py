from __future__ import annotations

import numpy as np

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable


class PFDrawOffsets(PFDrawable):

    def __init__(self,
                 decimal_places: int = 2,
                 color: str = "#CCCCCC",
                 x_offset: int = 0,
                 y_offset: int = 0,
                 interval: float = 10000):
        """Draws Bpms on the field

        Args:
            decimal_places: Decimal places to display
            color: The color of the text
            x_offset: Padding from the right
            y_offset: Padding from the top
            interval: MS Time between labels
        """
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.decimal_places = decimal_places
        self.color = color
        self.interval = interval

    def draw(self, pf: PlayField) -> PlayField:
        """Refer to __init__"""
        for offset in np.arange(0, pf.end, self.interval):
            txt = f"{offset:.{self.decimal_places}f}"
            w, h = pf.canvas_draw.textsize(txt)

            pf.canvas_draw.text(
                xy=pf.get_pos(offset,
                              column=pf.keys,
                              x_offset=self.x_offset,
                              y_offset=self.y_offset - h / 2),
                text=txt,
                fill=self.color
            )

        return pf
