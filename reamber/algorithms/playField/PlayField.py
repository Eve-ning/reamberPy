from typing import Union

from PIL import Image, ImageDraw, ImageColor

from reamber.algorithms.playField.parts.PFDrawable import PFDrawable
from reamber.bms.BMSMap import BMSMap
from reamber.o2jam.O2JMap import O2JMap
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMMap import SMMap


class PlayField:
    """Takes a chart and constructs an image from it using pillow"""

    HOLD_RESIZE_BUFFER: int = 2

    def __add__(self, other: PFDrawable):
        assert isinstance(other, PFDrawable), \
            "The added class must be an instance of PFDrawable!"
        return other.draw(pf=self)

    def __init__(self,
                 m: Union[OsuMap, O2JMap, SMMap, QuaMap, BMSMap],
                 duration_per_px: float = 5,
                 note_width: int = 10,
                 hit_height: int = 5,
                 hold_height: int = 5,
                 column_line_width: int = 1,
                 start_lead: float = 100.0,
                 end_lead: float = 100.0,
                 padding: int = 0,
                 background_color: str = "#000000"):
        """Creates an image of the chart

        Args:
            m: The map object
            duration_per_px: ms displayed / pixel. Larger values == lower zoom
            note_width: The width of each note in px
            hit_height: The height of each hit in px
            hold_height: The height of each hold head and tail in px
            start_lead: The ms lead before the first note.
                This is used to prevent clipping of the first note
            column_line_width: The width of column line separating columns
        """

        self.m = m
        self.duration_per_px = duration_per_px
        self.note_width = note_width
        self.hit_height = hit_height
        self.hold_height = hold_height
        self.column_line_width = column_line_width
        self.start_lead = start_lead
        self.end_lead = end_lead
        self.padding = padding
        self.background_color = background_color

        s = m.stack()
        keys = s.column.max() + 1

        start, end = s.offset.min(), s.offset.max()
        start -= start_lead
        end += end_lead
        duration = end - start

        canvas_w = int(
            note_width * keys + column_line_width * (keys - 1) + padding
        )  # -1 due to fencepost
        canvas_h = int(duration / duration_per_px)

        canvas = Image.new(mode='RGB', size=(canvas_w, canvas_h),
                           color=background_color)
        canvas_draw = ImageDraw.Draw(canvas, 'RGBA')

        self.keys = int(keys)
        self.start = start
        self.end = end
        self.duration = duration
        self.canvas_h = canvas_h
        self.canvas_w = canvas_w
        self.canvas = canvas
        self.canvas_draw = canvas_draw

    def get_pos(self, offset, column=0, x_offset=0, y_offset=0):
        return (
            int(column * (self.note_width + self.column_line_width))
            + x_offset,
            self.canvas_h - int((offset - self.start) / self.duration_per_px)
            - self.hit_height + y_offset
        )

    def export(self) -> Image.Image:
        """Exports the image directly

        See Also:
            export_fold for a folded image instead of a long rectangle
        """
        return self.canvas

    def export_fold(self,
                    max_height: int = 2000,
                    stage_line_width: int = 3,
                    stage_line_color: str = "#525252") -> Image.Image:
        """Exports by folding the image

        Args:
            max_height: Max height of the image.
            stage_line_width: The width of the stage line separator
            stage_line_color: The color of the stage line separator
        """
        # Split the canvas here into stages
        columns = int(self.canvas_h / max_height + 1)

        new_canvas_w = columns * self.canvas_w + \
                       (columns - 1) * stage_line_width
        new_canvas_h = max_height

        new_canvas = Image.new('RGB', (new_canvas_w, new_canvas_h),
                               color=ImageColor.getrgb(stage_line_color))

        for i in range(columns):
            chunk = self.canvas.crop(
                (0, self.canvas_h - (new_canvas_h * (i + 1)),
                 self.canvas_w + ((i + 1) * self.column_line_width) - i - 1,
                 self.canvas_h - new_canvas_h * i))

            new_canvas.paste(
                chunk,
                (i * (self.canvas_w + stage_line_width), 0)
            )

        return new_canvas
