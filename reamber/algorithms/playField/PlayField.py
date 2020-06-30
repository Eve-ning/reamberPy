""" Takes a chart and constructs an image from it using pillow """

from PIL import Image, ImageDraw, ImageColor
from reamber.osu.OsuMap import OsuMap
from reamber.sm.SMMapSet import SMMap
from reamber.o2jam.O2JMap import O2JMap
from reamber.quaver.QuaMap import QuaMap
from typing import Union

from reamber.algorithms.playField.parts.PFDrawable import PFDrawable

class PlayField:

    HOLD_RESIZE_BUFFER: int = 2

    def __add__(self, other: PFDrawable):
        assert isinstance(other, PFDrawable), "The added class must be an instance of PFDrawable!"
        return other.draw(pf=self)

    def __init__(self,
                 m: Union[OsuMap, O2JMap, SMMap, QuaMap],
                 durationPerPx: float = 5,
                 noteWidth: int = 10,
                 hitHeight: int = 5,
                 holdHeight: int = 5,
                 columnLineWidth: int  = 1,
                 startLead: float = 100.0,
                 endLead: float = 100.0,
                 padding: int = 0,
                 backgroundColor: str = "#000000"):
        """
        Creates an image of the chart

        :param m: The map object
        :param durationPerPx: ms displayed per pixel. The larger the value, the lower the zoom
        :param noteWidth: The width of each note in px
        :param hitHeight: The height of each hit in px
        :param holdHeight: The height of each hold head and tail in px
        :param startLead: The ms lead before the first note. This is used to prevent clipping of the first note
        :param columnLineWidth: The width of column line separating columns
        """

        self.m                = m
        self.durationPerPx    = durationPerPx
        self.noteWidth        = noteWidth
        self.hitHeight        = hitHeight
        self.holdHeight       = holdHeight
        self.columnLineWidth  = columnLineWidth
        self.startLead        = startLead
        self.endLead          = endLead
        self.padding          = padding
        self.backgroundColor  = backgroundColor

        keys = m.notes.maxColumn() + 1

        start, end = m.notes.firstLastOffset()
        start -= startLead
        end += endLead
        duration = end - start

        canvasW = int(noteWidth * keys + columnLineWidth * (keys - 1) + padding)  # -1 due to fencepost
        canvasH = int(duration / durationPerPx)

        canvas = Image.new(mode='RGB', size=(canvasW, canvasH), color=backgroundColor)
        canvasDraw = ImageDraw.Draw(canvas)

        self.keys       = keys
        self.start      = start
        self.end        = end
        self.duration   = duration
        self.canvasH    = canvasH
        self.canvasW    = canvasW
        self.canvas     = canvas
        self.canvasDraw = canvasDraw

    def export(self) -> Image.Image:
        """ Just grabs the image without modifications. I recommend exportFold to make it more squarish """
        return self.canvas

    def exportFold(self,
                   maxHeight: int = 2000,
                   stageLineWidth: int = 3,
                   stageLineColor: str = "#525252") -> Image.Image:
        """ Exports by folding the image

        :param maxHeight: The maximum height of the image, the lower this is, the wider the image
        :param stageLineWidth: The width of the stage line separator
        :param stageLineColor: The color of the stage line separator
        :return:
        """
        # Split the canvas here into stages
        columns = int(self.canvasH / maxHeight + 1)

        newCanvasW = columns * self.canvasW + (columns - 1) * stageLineWidth
        newCanvasH = maxHeight

        newCanvas = Image.new('RGB', (newCanvasW, newCanvasH),
                              color=ImageColor.getrgb(stageLineColor))

        """[SPLIT CANVAS]"""
        for i in range(columns):
            chunk = self.canvas.crop(
                (0                                                      , self.canvasH - (newCanvasH * (i + 1)),
                 self.canvasW + ((i + 1) * self.columnLineWidth) - i - 1, self.canvasH - newCanvasH * i))

            newCanvas.paste(chunk, (i * (self.canvasW + stageLineWidth) , 0))

        # We don't need to draw the column lines because the background already is the column lines

        return newCanvas



