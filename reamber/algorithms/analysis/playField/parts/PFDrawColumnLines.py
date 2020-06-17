from __future__ import annotations
from reamber.algorithms.analysis.playField import PlayField
from reamber.algorithms.analysis.playField.parts.PFDrawable import PFDrawable


class PFDrawColumnLines(PFDrawable):

    def __init__(self,
                 color: str = "#2b2b2b"):
        """ Draws column lines, separating columns of notes

        :param color: The color of the column lines
        """
        self.color = color
        # The reason we don't isolate width here is because the canvas size, note placement is dependent on it
        # so, we make it a PlayField prop

    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """

        for colLine in range(1, pf.keys):  # Fencepost again, if key = 4, we draw on 1 2 3
            for w in range(pf.columnLineWidth):
                pf.canvasDraw.line([(colLine * pf.noteWidth + (colLine - 1) * pf.columnLineWidth + w, 0),
                                    (colLine * pf.noteWidth + (colLine - 1) * pf.columnLineWidth + w, pf.canvasH)],
                                    fill=self.color)
        return pf
