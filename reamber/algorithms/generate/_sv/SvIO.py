from __future__ import annotations

from abc import ABC
from typing import Union, List, Type

from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap


class SvIO(ABC):
    """ Handles IO for SvSequence. """

    def write_as_sv(self, singular_type: Type, **kwargs) -> List:
        """ Writes the sequence as a
        List[singularType(offset=sv.offset, multiplier=sv.multiplier)]

        Must be able to accept 'offset' and 'multiplier' as argument.

        Allows **kwargs to input in every singularType during writing.

        Example::

            seq.write_as_sv(OsuSv, volume=20, kiai=True)

        Args:
            singular_type: Type of the singular obj
        """
        return [
            singular_type(offset=sv.offset, multiplier=sv.multiplier, **kwargs)
            for sv in self
        ]

    def write_as_bpm(self, singular_type: Type, multiplication: float = 1.0,
                     **kwargs) -> List:
        """ Writes the sequence
        as a List[singularType(offset=sv.offset, bpm=sv.multiplier)]

        Must be able to accept 'offset' and 'bpm' as argument.

        Allows **kwargs to input in every singularType during writing.

        Multiplication multiplies the multiplier before exporting.

        Example:
            seq.write_as_bpm(OsuBpm, volume=20, kiai=True)

        Args:
            singular_type: Type of the singular obj
            multiplication: Multiplier before exporting the sv as a BPM.
        """
        return [
            singular_type(offset=sv.offset, bpm=sv.multiplier * multiplication,
                          **kwargs)
            for sv in self
        ]

    @classmethod
    def read_sv_from_map(cls, m: Union[OsuMap, QuaMap]):
        """ Reads the scroll velocities from maps.

        Notes:
            Only some map types have scroll velocities
        """
        return cls([(sv.offset, sv.multiplier) for sv in m.svs])
