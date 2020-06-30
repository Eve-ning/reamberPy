from __future__ import annotations
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable


class PFDrawBpm(PFDrawable):

    def __init__(self,
                 decimalPlaces: int = 2,
                 color: str = "#cf6b4a",
                 xOffset: int = 0,
                 yOffset: int = 0):
        """ Draws Bpms on the field

        :param decimalPlaces: The number of decimal places to display
        :param color: The color of the text
        :param xOffset: Padding from the right, useful if you have multiple text drawables overlapping
        :param xOffset: Padding from the right, useful if you have multiple text drawables overlapping
        """
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.decimalPlaces = decimalPlaces
        self.color = color

    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """
        for bpm in pf.m.bpms:
            txt = f"{bpm.bpm:.{self.decimalPlaces}f}"
            w, h = pf.canvasDraw.textsize(txt)
            x = pf.canvasW - w - self.xOffset
            y = pf.canvasH - int((bpm.offset - pf.start) / pf.durationPerPx) - int(h/2) - self.yOffset

            pf.canvasDraw.text(xy=(x, y),
                               text=txt,
                               fill=self.color)

        return pf
