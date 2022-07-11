from __future__ import annotations

from reamber.base.Property import item_props
from reamber.base.RAConst import RAConst
from reamber.base.Timed import Timed


@item_props()
class Bpm(Timed):
    """A non-playable timed object indicating tempo of the map.

    Notes:
        This should not be used directly, instead, use subclassed Bpm classes
        specific for games. Such as ``OsuBpm`` or ``QuaBpm``.

    Examples:

        >>> b = Bpm(offset=1000, bpm=200, metronome=4)
        >>> b.offset, b.bpm, b.metronome
        (1000, 200, 4)

        >>> b.beat_length
        300.0

        >>> b.metronome_length
        1200.0
    """

    _props = dict(bpm=['float', 0.0],
                  metronome=['float', 4.0])

    def __init__(self, offset: float, bpm: float, metronome: float = 4,
                 **kwargs):
        """Initializer

        Args:
            offset: offset in ms
            bpm: BPM in beats per minute
            metronome: Metronome, can be float
        """
        super().__init__(offset=offset, bpm=bpm, metronome=metronome, **kwargs)

    @property
    def beat_length(self) -> float:
        """Get duration of each beat in ms

        Examples:

            >>> Bpm(offset=0, bpm=200, metronome=4).beat_length
            300.0
        """
        return RAConst.min_to_msec(1.0 / self.bpm)

    @property
    def metronome_length(self) -> float:
        """Get duration of each metronome in ms

        Notes:
            This is simply the ``beat_length`` * ``metronome``

        Examples:

            >>> Bpm(offset=0, bpm=200, metronome=4).metronome_length
            1200.0
        """
        return self.beat_length * self.metronome
