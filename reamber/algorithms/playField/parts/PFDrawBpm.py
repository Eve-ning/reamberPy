from __future__ import annotations

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable


class PFDrawBpm(PFDrawable):

    def __init__(self,
                 decimalPlaces: int = 2,
                 color: str = "#cf6b4a",
                 x_offset: int = 0,
                 y_offset: int = 0):
        """ Draws Bpms on the field

        :param decimalPlaces: The number of decimal places to display
        :param color: The color of the text
        :param x_offset: Padding from the right, useful if you have multiple text drawables overlapping
        :param y_offset: Padding from the bottom, useful if you have multiple text drawables overlapping
        """
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.decimal_places = decimalPlaces
        self.color = color

    # noinspection DuplicatedCode
    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """
        for bpm in pf.m.bpms:
            txt = f"{float(bpm.bpm):.{self.decimal_places}f}"
            w, h = pf.canvas_draw.textsize(txt)

            pf.canvas_draw.text(xy=pf.get_pos(bpm.offset,
                                              column=pf.keys,
                                              x_offset=self.x_offset,
                                              y_offset=self.y_offset - h / 2),
                                text=txt,
                                fill=self.color)

        return pf
