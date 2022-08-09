from __future__ import annotations

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap


class PFDrawSv(PFDrawable):

    def __init__(self,
                 decimal_places: int = 2,
                 color: str = "#4ef279",
                 x_offset: int = 0,
                 y_offset: int = 0):
        """Draws Svs on the field, only works with maps that have svs

        Args:
            decimal_places: The number of decimal places to display
            color: The color of the text
            x_offset: Padding from the right
            y_offset: The offset to move the text
        """
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.decimal_places = decimal_places
        self.color = color

    def draw(self, pf: PlayField) -> PlayField:
        """Refer to __init__"""
        assert isinstance(pf.m, OsuMap) or isinstance(pf.m, QuaMap), \
            "Only sv maps are supported."

        for sv in pf.m.svs:
            txt = f"{sv.multiplier:.{self.decimal_places}f}"
            _, h = pf.canvas_draw.textsize(txt)

            pf.canvas_draw.text(
                xy=pf.get_pos(sv.offset,
                              column=pf.keys,
                              x_offset=self.x_offset,
                              y_offset=self.y_offset - h / 2),
                text=txt,
                fill=self.color
            )

        return pf
