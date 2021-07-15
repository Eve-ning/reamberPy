from __future__ import annotations


from reamber.base.Hold import Hold
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuNoteMeta import OsuNoteMeta


class OsuHold(Hold, OsuNoteMeta):
    def __init__(self,
                 offset: float,
                 column: int,
                 length: float,
                 hitsound_set: int = OsuSampleSet.AUTO,
                 sample_set: int = OsuSampleSet.AUTO,
                 addition_set: int = OsuSampleSet.AUTO,
                 custom_set: int = OsuSampleSet.AUTO,
                 volume: int = 0,
                 hitsound_file: str = "",
                 **kwargs):
        super(OsuHold, self).__init__(
            offset=offset, column=column, length=length, hitsound_set=hitsound_set,
            sample_set=sample_set, addition_set=addition_set, custom_set=custom_set,
            volume=volume, hitsound_file=hitsound_file, **kwargs
        )

    @staticmethod
    def read_string(s: str, keys: int) -> OsuHold:
        """ Reads a single line under the [HitObjects] Label. This must explicitly be a Hold Object.

        keys must be specified for conversion of code value to actual column.

        :raises: ValueError if the string is not of the correct format.
        """

        if not OsuNoteMeta.is_hold(s):
            raise ValueError(f"String provided is not of the correct format for OsuHit. {s}")

        s_comma = s.split(",")
        s_colon = s_comma[-1].split(":")

        try:
            return OsuHold(
                offset=float(s_comma[2]),
                column=OsuNoteMeta.x_axis_to_column(int(s_comma[0]), keys),
                length=float(s_colon[0]) - float(s_comma[2]),
                hitsound_set=int(s_comma[4]),
                sample_set=int(s_colon[1]),
                addition_set=int(s_colon[2]),
                custom_set=int(s_colon[3]),
                volume=int(s_colon[4]),
                hitsound_file=s_colon[5]
            )
        except IndexError as e:
            raise ValueError(f"String provided is not of the correct format for OsuHold. {s}, {e.args}")

    def write_string(self, keys: int) -> str:
        """ Exports a .osu writable string """
        return f"{OsuNoteMeta.column_to_x_axis(self.column, keys=keys)},{192}," \
               f"{int(self.offset)},{128},{self.hitsound_set},{int(self.offset + self.length)}:" \
               f"{self.sample_set}:{self.addition_set}:{self.custom_set}:{self.volume}:{self.hitsound_file}"

    @staticmethod
    def _from_series_allowed_names():
        return [*Hold._from_series_allowed_names(),
                'hitsound_set',
                'sample_set',
                'addition_set',
                'custom_set',
                'volume',
                'hitsound_file']
