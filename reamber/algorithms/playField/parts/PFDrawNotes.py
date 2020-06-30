from __future__ import annotations
from PIL import Image, ImageDraw

from reamber.algorithms.playField.parts.PFDrawable import PFDrawable
from reamber.algorithms.playField import PlayField

class PFDrawNotes(PFDrawable):

    COL_DICT = [[0],
                [1,0],
                [0,2,0],
                [0,1,1,0],
                [0,1,2,1,0],
                [0,1,0,0,1,0],
                [0,1,0,2,0,1,0],
                [0,1,0,1,1,0,1,0],
                [0,1,0,1,2,1,0,1,0],
                [0,1,0,1,0,0,1,0,1,0],
                [0,1,0,1,0,2,0,1,0,1,0],
                [0,1,0,1,0,1,1,0,1,0,1,0],
                [0,1,0,1,0,1,2,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,2,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1,2,1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,0]]

    def __init__(self,
                 img0OutlineColor: str = "#47fcff",
                 img0FillColor: str    = "#28b5b8",
                 img1OutlineColor: str = "#ffffff",
                 img1FillColor: str    = "#c2c2c2",
                 img2OutlineColor: str = "#f8ff30",
                 img2FillColor: str    = "#adb31e",
                 outlineWidth: int     = 2):
        """ The draws all the notes on the field

        The color used for each column is specified in the COL_DICT

        :param img0OutlineColor: The color to outline the first note image
        :param img0FillColor: The color to fill the first note image
        :param img1OutlineColor: The color to outline the second note image
        :param img1FillColor: The color to fill the second note image
        :param img2OutlineColor: The color to outline the third note image
        :param img2FillColor: The color to fill the third note image
        :param outlineWidth: The width of each outline. 0 for no outline
        """
        self.outlineWidth     = outlineWidth
        self.img0OutlineColor = img0OutlineColor
        self.img0FillColor    = img0FillColor
        self.img1OutlineColor = img1OutlineColor
        self.img1FillColor    = img1FillColor
        self.img2OutlineColor = img2OutlineColor
        self.img2FillColor    = img2FillColor

    def draw(self, pf: PlayField) -> PlayField:
        """ Refer to __init__ """

        imgs = [self._createNoteSet(pf=pf, fillColor=self.img0FillColor, outlineColor=self.img0OutlineColor,
                                    width=self.outlineWidth),
                self._createNoteSet(pf=pf, fillColor=self.img1FillColor, outlineColor=self.img1OutlineColor,
                                    width=self.outlineWidth),
                self._createNoteSet(pf=pf, fillColor=self.img2FillColor, outlineColor=self.img2OutlineColor,
                                    width=self.outlineWidth)]

        self._drawHits(imgs, pf)
        self._drawHolds(imgs, pf)

        return pf

    def _drawHits(self, imgs, pf: PlayField):
        for hit in pf.m.notes.hits():
            hitImg = imgs[self.COL_DICT[pf.keys - 1][hit.column]]['hit']
            pf.canvas.paste(hitImg,
                            (int(hit.column * (pf.noteWidth + pf.columnLineWidth)),
                            pf.canvasH - int((hit.offset - pf.start) / pf.durationPerPx) - pf.hitHeight),
                            hitImg)

    def _drawHolds(self, imgs, pf: PlayField):
        for hold in pf.m.notes.holds():
            holdHeadImg = imgs[self.COL_DICT[pf.keys - 1][hold.column]]['holdH']

            # DRAWS THE HEAD
            pf.canvas.paste(holdHeadImg,
                            (int(hold.column * (pf.noteWidth + pf.columnLineWidth)),
                            pf.canvasH - int((hold.offset - pf.start) / pf.durationPerPx) - pf.holdHeight),
                            holdHeadImg)

            holdTailImg = imgs[self.COL_DICT[pf.keys - 1][hold.column]]['holdT']

            # DRAWS THE TAIL
            pf.canvas.paste(holdTailImg,
                            (int(hold.column * (pf.noteWidth + pf.columnLineWidth)),
                            pf.canvasH - int((hold.tailOffset() - pf.start) / pf.durationPerPx) - pf.holdHeight),
                            holdTailImg)

            # DRAWS THE BODY
            holdImgHeight = int(hold.length / pf.durationPerPx) - pf.holdHeight + pf.HOLD_RESIZE_BUFFER

            # If too short we don't draw it
            if holdImgHeight > 0:
                holdImg = imgs[self.COL_DICT[pf.keys - 1][hold.column]]['holdB'].resize((pf.noteWidth, holdImgHeight))

                pf.canvas.paste(holdImg,
                                (int(hold.column * (pf.noteWidth + pf.columnLineWidth)),
                                pf.canvasH - int((hold.tailOffset() - pf.start) / pf.durationPerPx)),
                                holdImg)

    @staticmethod
    def _createHit(pf: PlayField, fillColor, outlineColor, width=4):
        img = Image.new(mode='RGBA', size=(pf.noteWidth, pf.hitHeight), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        path = [(0, 0),
                (0, pf.hitHeight - 1),
                (pf.noteWidth - 1, pf.hitHeight - 1),
                (pf.noteWidth - 1, 0),
                (0, 0)]
        draw.polygon(path, fill=fillColor)
        draw.line(path, fill=outlineColor, width=width)
        return img

    @staticmethod
    def _createHoldHead(pf: PlayField, fillColor, outlineColor, width=4):
        img = Image.new(mode='RGBA', size=(pf.noteWidth, pf.holdHeight), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        path = [(0, 0),
                (int(pf.noteWidth * 1 / 3), pf.holdHeight - int(width / 2)),
                (int(pf.noteWidth * 2 / 3), pf.holdHeight - int(width / 2)),
                (pf.noteWidth - 1, 0)]

        draw.polygon(path, fill=fillColor)
        draw.line(path, fill=outlineColor, width=width)
        return img

    @staticmethod
    def _createHoldBody(pf: PlayField, fillColor, outlineColor, width=4):
        img = Image.new(mode='RGBA', size=(pf.noteWidth, pf.holdHeight), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon([(0, 0),
                      (0, pf.noteWidth - 1),
                      (pf.noteWidth - 1, pf.hitHeight - 1),
                      (pf.noteWidth - 1, 0)],
                     fill=fillColor)
        draw.line([(0, 0),
                   (0, pf.holdHeight)],
                  fill=outlineColor, width=width)
        draw.line([(pf.noteWidth - 2, 0),
                   (pf.noteWidth - 2, pf.holdHeight)],
                  fill=outlineColor, width=width)
        return img

    @classmethod
    def _createHoldTail(cls, pf: PlayField, fillColor, outlineColor, width=4):
        """ It's just the inverted head """
        return cls._createHoldHead(pf, fillColor, outlineColor, width).transpose(Image.FLIP_TOP_BOTTOM)

    @classmethod
    def _createNoteSet(cls, pf: PlayField, fillColor, outlineColor, width=4):
        return {'hit': cls._createHit(pf, fillColor, outlineColor, width),
                'holdH': cls._createHoldHead(pf, fillColor, outlineColor, width),
                'holdB': cls._createHoldBody(pf, fillColor, outlineColor, width),
                'holdT': cls._createHoldTail(pf, fillColor, outlineColor, width)}
