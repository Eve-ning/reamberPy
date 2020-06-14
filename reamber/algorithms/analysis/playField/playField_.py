""" Takes a chart and constructs an image from it using pillow

All images provided in rsc/images/skins/ must be of the same size.
Yes, even holds.

"""

from PIL import Image, ImageDraw, ImageColor, ImageFont
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.sm.SMMapSetObj import SMMapObj
from reamber.o2jam.O2JMapObj import O2JMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.base.RAConst import RAConst
from reamber.algorithms.analysis.bpm.bpmBeatOffsets import bpmBeatOffsets
from typing import overload, List

@overload
def playField(m: SMMapObj, durationPerPx: float = 5, maxHeight: int = 3000, noteWidth: int = 10, hitHeight: int = 5,
              holdHeight: int = 5, outlineWidth: int = 2, imgAOutlineColor: str = "#47fcff", imgAFillColor: str = "#28b5b8",
              imgBOutlineColor: str = "#ffffff", imgBFillColor: str = "#c2c2c2", imgCOutlineColor: str = "#f8ff30",
              imgCFillColor: str = "#adb31e", startLead: float = 100.0, columnLineWidth: int = 1,
              columnLineColor: str = "#2b2b2b", stageLineWidth: int = 3, stageLineColor: str = "#525252",
              beatLines: List = None) -> Image.Image: ...
@overload
def playField(m: O2JMapObj, durationPerPx: float = 5, maxHeight: int = 3000, noteWidth: int = 10, hitHeight: int = 5,
              holdHeight: int = 5, outlineWidth: int = 2, imgAOutlineColor: str = "#47fcff", imgAFillColor: str = "#28b5b8",
              imgBOutlineColor: str = "#ffffff", imgBFillColor: str = "#c2c2c2", imgCOutlineColor: str = "#f8ff30",
              imgCFillColor: str = "#adb31e", startLead: float = 100.0, columnLineWidth: int = 1,
              columnLineColor: str = "#2b2b2b", stageLineWidth: int = 3, stageLineColor: str = "#525252",
              beatLines: List = None) -> Image.Image: ...
@overload
def playField(m: QuaMapObj, durationPerPx: float = 5, maxHeight: int = 3000, noteWidth: int = 10, hitHeight: int = 5,
              holdHeight: int = 5, outlineWidth: int = 2, imgAOutlineColor: str = "#47fcff", imgAFillColor: str = "#28b5b8",
              imgBOutlineColor: str = "#ffffff", imgBFillColor: str = "#c2c2c2", imgCOutlineColor: str = "#f8ff30",
              imgCFillColor: str = "#adb31e", startLead: float = 100.0, columnLineWidth: int = 1,
              columnLineColor: str = "#2b2b2b", stageLineWidth: int = 3, stageLineColor: str = "#525252",
              beatLines: List = None) -> Image.Image: ...
@overload
def playField(m: OsuMapObj, durationPerPx: float = 5, maxHeight: int = 3000, noteWidth: int = 10, hitHeight: int = 5,
              holdHeight: int = 5, outlineWidth: int = 2, imgAOutlineColor: str = "#47fcff", imgAFillColor: str = "#28b5b8",
              imgBOutlineColor: str = "#ffffff", imgBFillColor: str = "#c2c2c2", imgCOutlineColor: str = "#f8ff30",
              imgCFillColor: str = "#adb31e", startLead: float = 100.0, columnLineWidth: int = 1,
              columnLineColor: str = "#2b2b2b", stageLineWidth: int = 3, stageLineColor: str = "#525252",
              beatLines: List = None) -> Image.Image: ...
def playField(m: OsuMapObj,
              durationPerPx: float  = 5,
              maxHeight: int        = 2000,
              noteWidth: int        = 10,
              hitHeight: int        = 5,
              holdHeight: int       = 5,
              outlineWidth: int     = 2,
              imgAOutlineColor: str = "#47fcff",
              imgAFillColor: str    = "#28b5b8",
              imgBOutlineColor: str = "#ffffff",
              imgBFillColor: str    = "#c2c2c2",
              imgCOutlineColor: str = "#f8ff30",
              imgCFillColor: str    = "#adb31e",
              startLead: float      = 100.0,
              columnLineWidth: int  = 1,
              columnLineColor: str  = "#2b2b2b",
              stageLineWidth: int   = 3,
              stageLineColor: str   = "#525252",
              beatLines: List       = None,
              displaySvs: bool      = True,
              svColor: str          = "#4ef279",
              displayBpms: bool     = True,
              bpmColor: str         = "#cf6b4a"
              ) -> Image.Image:
    """
    Creates an image of the chart

    :param m: The map object
    :param durationPerPx: ms displayed per pixel. The larger the value, the lower the zoom
    :param maxHeight: The maximum height of the image. The lower the value, the wider the image
    :param noteWidth: The width of each note in px
    :param hitHeight: The height of each hit in px
    :param holdHeight: The height of each hold head and tail in px
    :param outlineWidth: The thickness of each outline
    :param imgAOutlineColor: The outline color of Note A
    :param imgAFillColor: The fill color of Note A
    :param imgBOutlineColor: The outline color of Note B
    :param imgBFillColor: The fill color of Note B
    :param imgCOutlineColor: The outline color of Note C
    :param imgCFillColor: The fill color of Note C
    :param startLead: The ms lead before the first note. This is used to prevent clipping of the first note
    :param columnLineWidth: The width of column line separating columns
    :param columnLineColor: The color of column line separating columns
    :param stageLineWidth: The width of column line separating stages
    :param stageLineColor: The color of column line separating stages
    :param beatLines: The snaps to be displayed
    :param displaySvs: Whether SVs should be displayed
    :param svColor: Color of Text SVs displayed
    :param displayBpms: Whether BPMs should be displayed
    :param bpmColor: Color of Bpms displayed
    :return: A savable image
    """
    def _createHit(fillColor, outlineColor, width=4):
        img = Image.new(mode='RGBA', size=(noteWidth, hitHeight), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        path = [(0, 0),
                (0, hitHeight - 1),
                (noteWidth - 1, hitHeight - 1),
                (noteWidth - 1, 0),
                (0, 0)]
        draw.polygon(path, fill=fillColor)
        draw.line(path, fill=outlineColor, width=width)
        return img

    def _createHoldBody(fillColor, outlineColor, width=4):
        img = Image.new(mode='RGBA', size=(noteWidth, holdHeight), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon([(0, 0),
                      (0, noteWidth - 1),
                      (noteWidth - 1, hitHeight - 1),
                      (noteWidth - 1, 0)],
                     fill=fillColor)
        draw.line([(0, 0),
                   (0, holdHeight)],
                  fill=outlineColor, width=width)
        draw.line([(noteWidth - 2, 0),
                   (noteWidth - 2, holdHeight)],
                  fill=outlineColor, width=width)
        return img

    def _createHoldHead(fillColor, outlineColor, width=4):
        img = Image.new(mode='RGBA', size=(noteWidth, holdHeight), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        path = [(0, 0),
                (int(noteWidth * 1 / 3), holdHeight - int(width / 2)),
                (int(noteWidth * 2 / 3), holdHeight - int(width / 2)),
                (noteWidth - 1, 0)]

        draw.polygon(path, fill=fillColor)
        draw.line(path, fill=outlineColor, width=width)
        return img

    def _createHoldTail(fillColor, outlineColor, width=4):
        return _createHoldHead(fillColor, outlineColor, width).transpose(Image.FLIP_TOP_BOTTOM)

    def _createNoteSet(fillColor, outlineColor, width=4):
        return _createHit(fillColor, outlineColor, width),\
               (_createHoldHead(fillColor, outlineColor, width),
                _createHoldBody(fillColor, outlineColor, width),
                _createHoldTail(fillColor, outlineColor, width))

    IMG_A, IMG_AH = _createNoteSet(fillColor=imgAFillColor, outlineColor=imgAOutlineColor, width=outlineWidth)
    IMG_B, IMG_BH = _createNoteSet(fillColor=imgBFillColor, outlineColor=imgBOutlineColor, width=outlineWidth)
    IMG_C, IMG_CH = _createNoteSet(fillColor=imgCFillColor, outlineColor=imgCOutlineColor, width=outlineWidth)

    HIT_DICT = [{0: IMG_A}
              , {0: IMG_A, 1: IMG_B}
              , {0: IMG_A, 1: IMG_C, 2: IMG_A}
              , {0: IMG_A, 1: IMG_B, 2: IMG_B, 3: IMG_A}
              , {0: IMG_A, 1: IMG_B, 2: IMG_C, 3: IMG_B, 4: IMG_A}
              , {0: IMG_A, 1: IMG_B, 2: IMG_A, 3: IMG_A, 4: IMG_B, 5: IMG_A}
              , {0: IMG_A, 1: IMG_B, 2: IMG_A, 3: IMG_C, 4: IMG_A, 5: IMG_B, 6: IMG_A}
              , {0: IMG_A, 1: IMG_B, 2: IMG_A, 3: IMG_B, 4: IMG_B, 5: IMG_A, 6: IMG_B, 7: IMG_A}
              , {0: IMG_A, 1: IMG_B, 2: IMG_A, 3: IMG_B, 4: IMG_C, 5: IMG_B, 6: IMG_A, 7: IMG_B, 8: IMG_A}]

    HOLD_DICT = [{0: IMG_AH}
               , {0: IMG_AH, 1: IMG_BH}
               , {0: IMG_AH, 1: IMG_CH, 2: IMG_AH}
               , {0: IMG_AH, 1: IMG_BH, 2: IMG_BH, 3: IMG_AH}
               , {0: IMG_AH, 1: IMG_BH, 2: IMG_CH, 3: IMG_BH, 4: IMG_AH}
               , {0: IMG_AH, 1: IMG_BH, 2: IMG_AH, 3: IMG_AH, 4: IMG_BH, 5: IMG_AH}
               , {0: IMG_AH, 1: IMG_BH, 2: IMG_AH, 3: IMG_CH, 4: IMG_AH, 5: IMG_BH, 6: IMG_AH}
               , {0: IMG_AH, 1: IMG_BH, 2: IMG_AH, 3: IMG_BH, 4: IMG_BH, 5: IMG_AH, 6: IMG_BH, 7: IMG_AH}
               , {0: IMG_AH, 1: IMG_BH, 2: IMG_AH, 3: IMG_BH, 4: IMG_CH, 5: IMG_BH, 6: IMG_AH, 7: IMG_BH, 8: IMG_AH}]

    # Buffer for image resizing of holds do not change!
    HOLD_RESIZE_BUFFER = 2

    keys = m.notes.maxColumn() + 1

    start, end = m.notes.firstLastOffset()
    start -= startLead
    duration = end - start

    canvasW = int(noteWidth * keys + columnLineWidth * (keys - 1))  # -1 due to fencepost
    canvasH = int(duration / durationPerPx)

    canvas = Image.new(mode='RGB', size=(canvasW, canvasH))
    canvasDraw = ImageDraw.Draw(canvas)

    """[DRAW COLUMN LINES]"""
    for colLine in range(1, keys):  # Fencepost again, if key = 4, we draw on 1 2 3
        for w in range(columnLineWidth):
            canvasDraw.line([(colLine * noteWidth + (colLine - 1) * columnLineWidth + w, 0),
                             (colLine * noteWidth + (colLine - 1) * columnLineWidth + w, canvasH)],
                            fill=columnLineColor)

    """[DRAW BEAT LINES]"""
    # Need to draw it from most common to least common, else it'll overlap incorrectly
    if beatLines:
        for beatLine in sorted(beatLines, reverse=True):
            nth = beatLine

            if beatLine not in RAConst.DIVISION_COLOR.keys(): color = "#666666"  # Default color if val not found
            else: color = RAConst.DIVISION_COLOR[beatLine]

            for beat in bpmBeatOffsets(m.bpms, nths=nth, lastOffset=m.notes.lastOffset()):
                canvasDraw.line([(0, canvasH - int((beat - start) / durationPerPx)),
                                 (canvasW, canvasH - int((beat - start) / durationPerPx))],
                                fill=color)

    if displayBpms:
        """[DRAW BPMs]"""
        for bpm in m.bpms:
            txt = f"{bpm.bpm:.2f}"
            w, h = canvasDraw.textsize(txt)
            canvasDraw.text(xy=(canvasW - w, canvasH - int((bpm.offset - start) / durationPerPx) - h),
                            text=f"{bpm.bpm:.2f}",
                            fill=bpmColor)

    if displaySvs and (isinstance(m, OsuMapObj) or isinstance(m, QuaMapObj)):
        """[DRAW SVS]"""
        for sv in m.svs:
            canvasDraw.text(xy=(0, canvasH - int((sv.offset - start) / durationPerPx)),
                            text=f"{sv.multiplier:.2f}",
                            fill=svColor)

    """[DRAW NOTES]"""
    for hit in m.notes.hits():
        hitImg = HIT_DICT[keys - 1][hit.column]
        canvas.paste(hitImg,
                     (int(hit.column * (noteWidth + columnLineWidth)),
                      canvasH - int((hit.offset - start) / durationPerPx) - hitHeight),
                     hitImg)

    for hold in m.notes.holds():
        holdHeadImg = HOLD_DICT[keys - 1][hold.column][0]

        canvas.paste(holdHeadImg,
                     (int(hold.column * (noteWidth + columnLineWidth)),
                      canvasH - int((hold.offset - start) / durationPerPx) - holdHeight),
                     holdHeadImg)

        holdTailImg = HOLD_DICT[keys - 1][hold.column][2]

        canvas.paste(holdTailImg,
                     (int(hold.column * (noteWidth + columnLineWidth)),
                      canvasH - int((hold.tailOffset() - start) / durationPerPx) - holdHeight),
                     holdTailImg)

        holdImgHeight = int(hold.length / durationPerPx) - holdHeight + HOLD_RESIZE_BUFFER
        if holdImgHeight > 0:
            holdImg = HOLD_DICT[keys - 1][hold.column][1] \
                .resize((noteWidth, holdImgHeight))

            canvas.paste(holdImg,
                         (int(hold.column * (noteWidth + columnLineWidth)),
                          canvasH - int((hold.tailOffset() - start) / durationPerPx)),
                         holdImg)

    # Split the canvas here into stages
    columns = int(canvasH / maxHeight + 1)

    newCanvasW = columns * canvasW + (columns - 1) * stageLineWidth
    newCanvasH = maxHeight

    newCanvas = Image.new('RGB', (newCanvasW, newCanvasH),
                          color=ImageColor.getrgb(stageLineColor))

    """[SPLIT CANVAS]"""
    for i in range(columns):
        chunk = canvas.crop((0, canvasH - (newCanvasH * (i + 1)),
                             canvasW + ((i + 1) * columnLineWidth) - i - 1, canvasH - newCanvasH * i))
        newCanvas.paste(chunk, (i * (canvasW + stageLineWidth) , 0))

    # We don't need to draw the column lines because the background already is the column lines

    return newCanvas



