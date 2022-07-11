from __future__ import annotations

from reamber.base import item_props
from reamber.base.Hit import Hit
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSampleSet import OsuSampleSet


@item_props()
class OsuHit(Hit, OsuNoteMeta):

    def __init__(self,
                 offset: float,
                 column: int,
                 hitsound_set: int = OsuSampleSet.AUTO,
                 sample_set: int = OsuSampleSet.AUTO,
                 addition_set: int = OsuSampleSet.AUTO,
                 custom_set: int = 0,
                 volume: int = 0,
                 hitsound_file: str = "",
                 **kwargs):
        super().__init__(
            offset=offset, column=column, hitsound_set=hitsound_set,
            sample_set=sample_set, addition_set=addition_set,
            custom_set=custom_set, volume=volume,
            hitsound_file=hitsound_file, **kwargs
        )

    @staticmethod
    def read_string(s: str, keys: int, as_dict: bool = False) -> OsuHit:
        """Reads a single line under the [HitObject] Label"""

        if not OsuNoteMeta.is_hit(s):
            raise ValueError(f"Bad OsuHit Format. {s}")

        s_comma = s.split(",")
        s_colon = s_comma[-1].split(":")

        d = dict(
            offset=float(s_comma[2]),
            column=OsuNoteMeta.x_axis_to_column(int(s_comma[0]), keys),
            hitsound_set=int(s_comma[4]),
            sample_set=int(s_colon[0]),
            addition_set=int(s_colon[1]),
            custom_set=int(s_colon[2]),
            volume=int(s_colon[3]),
            hitsound_file=s_colon[4]
        )
        return d if as_dict else OsuHit(**d)

    def write_string(self, keys: int) -> str:
        """Exports a .osu writable string"""
        return f"{OsuNoteMeta.column_to_x_axis(self.column, keys=keys)}," \
               f"{192}," \
               f"{int(self.offset)}," \
               f"{1}," \
               f"{int(self.hitsound_set)}," \
               f"{int(self.sample_set)}:" \
               f"{int(self.addition_set)}:" \
               f"{int(self.custom_set)}:" \
               f"{int(self.volume)}:" \
               f"{self.hitsound_file}"
