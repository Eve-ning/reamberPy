from __future__ import annotations

from reamber.base.Property import item_props
from reamber.base.RAConst import RAConst
from reamber.base.Timed import Timed


@item_props()
class Bpm(Timed):
    """ A non-playable timed object that specifies the tempo of the map.

    This is synonymous with Bpm Point, it's named Object to make it consistent
    """

    _props = dict(bpm=['float', 0.0],
                  metronome=['float', 4.0])

    def __init__(self, offset: float, bpm: float, metronome: float = 4, **kwargs):
        super().__init__(offset=offset, bpm=bpm, metronome=metronome, **kwargs)

    @property
    def beat_length(self) -> float:
        """ Returns the length of the beat in ms """
        return RAConst.min_to_msec(1.0 / self.bpm)

    @property
    def metronome_length(self) -> float:
        """ Returns the length of the metronome in ms """
        return self.beat_length * self.metronome

