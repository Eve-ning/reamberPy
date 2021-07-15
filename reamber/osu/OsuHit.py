from __future__ import annotations


from reamber.base.Hit import Hit
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuNoteMeta import OsuNoteMeta


class OsuHit(Hit, OsuNoteMeta):

    def __init__(self,
                 offset: float,
                 column: int,
                 hitsound_set: int = OsuSampleSet.AUTO,
                 sample_set: int = OsuSampleSet.AUTO,
                 addition_set: int = OsuSampleSet.AUTO,
                 custom_set: int = OsuSampleSet.AUTO,
                 volume: int = 0,
                 hitsound_file: str = "",
                 **kwargs):
        super(OsuHit, self).__init__(
            offset=offset, column=column, hitsound_set=hitsound_set, sample_set=sample_set,
            addition_set=addition_set, custom_set=custom_set, volume=volume,
            hitsound_file=hitsound_file, **kwargs
        )

    @staticmethod
    def read_string(s: str, keys: int) -> OsuHit:
        """ Reads a single line under the [HitObject] Label. This must explicitly be a Hit Object.

        keys must be specified for conversion of code value to actual column.

        :raises: ValueError if the string is not of the correct format.
        """

        if not OsuNoteMeta.is_hit(s): raise ValueError(f"String provided is not of the correct format for OsuHit. {s}")

        s_comma = s.split(",")
        s_colon = s_comma[-1].split(":")

        try:
            return OsuHit(
                offset=float(s_comma[2]),
                column=OsuNoteMeta.x_axis_to_column(int(s_comma[0]), keys),
                hitsound_set=int(s_comma[4]),
                sample_set=int(s_colon[0]),
                addition_set=int(s_colon[1]),
                custom_set=int(s_colon[2]),
                volume=int(s_colon[3]),
                hitsound_file=s_colon[4]
            )
        except IndexError as e:
            raise ValueError(f"String provided is not of the correct format. {s}, {e.args}")

    def write_string(self, keys: int) -> str:
        """ Exports a .osu writable string """
        return f"{OsuNoteMeta.column_to_x_axis(self.column, keys=keys)},{192}," \
               f"{int(self.offset)},{1},{self.hitsound_set},{self.sample_set}:" \
               f"{self.addition_set}:{self.custom_set}:{self.volume}:{self.hitsound_file}"

    @staticmethod
    def _from_series_allowed_names():
        return [*Hit._from_series_allowed_names(),
                'hitsound_set',
                'sample_set',
                'addition_set',
                'custom_set',
                'volume',
                'hitsound_file']
