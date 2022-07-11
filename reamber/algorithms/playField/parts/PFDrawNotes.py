from __future__ import annotations

from PIL import Image, ImageDraw

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts.PFDrawable import PFDrawable


class PFDrawNotes(PFDrawable):
    COL_DICT = [[0],
                [1, 0],
                [0, 2, 0],
                [0, 1, 1, 0],
                [0, 1, 2, 1, 0],
                [0, 1, 0, 0, 1, 0],
                [0, 1, 0, 2, 0, 1, 0],
                [0, 1, 0, 1, 1, 0, 1, 0],
                [0, 1, 0, 1, 2, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0]]

    def __init__(self,
                 img0_outline_color: str = "#47fcff",
                 img0_fill_color: str = "#28b5b8",
                 img1_outline_color: str = "#ffffff",
                 img1_fill_color: str = "#c2c2c2",
                 img2_outline_color: str = "#f8ff30",
                 img2_fill_color: str = "#adb31e",
                 outline_width: int = 2):
        """The draws all the notes on the field

        The color used for each column is specified in the COL_DICT

        Args:
            img0_outline_color: The color to outline the first note image
            img0_fill_color: The color to fill the first note image
            img1_outline_color: The color to outline the second note image
            img1_fill_color: The color to fill the second note image
            img2_outline_color: The color to outline the third note image
            img2_fill_color: The color to fill the third note image
            outline_width: The width of each outline. 0 for no outline
        """
        self.outline_width = outline_width
        self.img0_outline_color = img0_outline_color
        self.img0_fill_color = img0_fill_color
        self.img1_outline_color = img1_outline_color
        self.img1_fill_color = img1_fill_color
        self.img2_outline_color = img2_outline_color
        self.img2_fill_color = img2_fill_color

    def draw(self, pf: PlayField) -> PlayField:
        """Refer to __init__"""

        imgs = [self._create_note_set(pf=pf, fill_color=self.img0_fill_color,
                                      outline_color=self.img0_outline_color,
                                      width=self.outline_width),
                self._create_note_set(pf=pf, fill_color=self.img1_fill_color,
                                      outline_color=self.img1_outline_color,
                                      width=self.outline_width),
                self._create_note_set(pf=pf, fill_color=self.img2_fill_color,
                                      outline_color=self.img2_outline_color,
                                      width=self.outline_width)]

        self._draw_hits(imgs, pf)
        self._draw_holds(imgs, pf)

        return pf

    def _draw_hits(self, imgs, pf: PlayField):
        for hit in pf.m.hits:
            hit_img = imgs[self.COL_DICT[int(pf.keys) - 1][int(hit.column)]][
                'hit']
            pf.canvas.paste(hit_img,
                            pf.get_pos(hit.offset, hit.column,
                                       y_offset=-pf.hit_height),
                            hit_img)

    def _draw_holds(self, imgs, pf: PlayField):
        for hold in pf.m.holds:
            hold_head_img = \
                imgs[self.COL_DICT[int(pf.keys) - 1]
                [int(hold.column)]]['holdH']

            # DRAWS THE HEAD
            pf.canvas.paste(
                hold_head_img,
                pf.get_pos(hold.offset, hold.column, y_offset=-pf.hold_height),
                hold_head_img
            )

            hold_tail_img = \
                imgs[self.COL_DICT[int(pf.keys) - 1]
                [int(hold.column)]]['holdT']

            # DRAWS THE TAIL
            pf.canvas.paste(hold_tail_img,
                            pf.get_pos(hold.tail_offset, hold.column,
                                       y_offset=-pf.hold_height),
                            hold_tail_img)

            # DRAWS THE BODY
            hold_img_height = int(hold.length / pf.duration_per_px) \
                              - pf.hold_height + pf.HOLD_RESIZE_BUFFER

            # If too short we don't draw it
            if hold_img_height > 0:
                hold_img = \
                    imgs[self.COL_DICT[int(pf.keys) - 1]
                    [int(hold.column)]]['holdB'].resize(
                        (pf.note_width, hold_img_height)
                    )

                pf.canvas.paste(hold_img,
                                pf.get_pos(hold.tail_offset, hold.column),
                                hold_img)

    @staticmethod
    def _create_hit(pf: PlayField, fill_color, outline_color, width=4):
        img = Image.new(mode='RGBA', size=(pf.note_width, pf.hit_height),
                        color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        path = [(0, 0),
                (0, pf.hit_height - 1),
                (pf.note_width - 1, pf.hit_height - 1),
                (pf.note_width - 1, 0),
                (0, 0)]
        draw.polygon(path, fill=fill_color)
        draw.line(path, fill=outline_color, width=width)
        return img

    @staticmethod
    def _create_hold_head(pf: PlayField, fill_color, outline_color, width=4):
        img = Image.new(mode='RGBA', size=(pf.note_width, pf.hold_height),
                        color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        path = [(0, 0),
                (int(pf.note_width * 1 / 3), pf.hold_height - int(width / 2)),
                (int(pf.note_width * 2 / 3), pf.hold_height - int(width / 2)),
                (pf.note_width - 1, 0)]

        draw.polygon(path, fill=fill_color)
        draw.line(path, fill=outline_color, width=width)
        return img

    @staticmethod
    def _create_hold_body(pf: PlayField, fill_color, outline_color, width=4):
        img = Image.new(mode='RGBA', size=(pf.note_width, pf.hold_height),
                        color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon([(0, 0),
                      (0, pf.note_width - 1),
                      (pf.note_width - 1, pf.hit_height - 1),
                      (pf.note_width - 1, 0)],
                     fill=fill_color)
        draw.line([(0, 0),
                   (0, pf.hold_height)],
                  fill=outline_color, width=width)
        draw.line([(pf.note_width - 2, 0),
                   (pf.note_width - 2, pf.hold_height)],
                  fill=outline_color, width=width)
        return img

    @classmethod
    def _create_hold_tail(cls, pf: PlayField, fill_color, outline_color,
                          width=4):
        """It's just the inverted head"""
        return cls._create_hold_head(pf, fill_color, outline_color,
                                     width).transpose(Image.FLIP_TOP_BOTTOM)

    @classmethod
    def _create_note_set(cls, pf: PlayField, fill_color, outline_color,
                         width=4):
        return {
            'hit': cls._create_hit(pf, fill_color, outline_color, width),
            'holdH': cls._create_hold_head(pf, fill_color, outline_color,
                                           width),
            'holdB': cls._create_hold_body(pf, fill_color, outline_color,
                                           width),
            'holdT': cls._create_hold_tail(pf, fill_color, outline_color,
                                           width)
        }
