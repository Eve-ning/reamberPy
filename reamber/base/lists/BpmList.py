from __future__ import annotations

from typing import TypeVar

import numpy as np

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.base.Bpm import Bpm
from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList

Item = TypeVar('Item')


@list_props(Bpm)
class BpmList(TimedList[Item]):
    def current_bpm(self, offset: float, sort=True, delta=0.1) -> Bpm:
        """ Finds the current BPM of the offset

        Args:
            offset: Offset to find associated bpm
            sort: Whether to sort the bpm implicitly. IT MUST BE SORTED!
            delta: A buffer for rounding errors

        Returns:
            The Bpm Class.
        """

        bpms = self.sorted() if sort else self
        # noinspection PyTypeChecker
        ix = int((np.sum((bpms.offset - offset - delta) <= 0)) - 1)
        if ix < 0: raise IndexError(
            f"Offset {offset} does not have a Bpm Associated with it.")
        return bpms[ix]

    def to_timing_map(self) -> TimingMap:
        return TimingMap.from_bpm_changes_offset(
            bpm_changes_offset=[
                BpmChangeOffset(b, m, o)
                for b, m, o in zip(self.bpm, self.metronome, self.offset)
            ]
        )

    def ave_bpm(self, last_offset: float = None) -> float:
        """ Calculates the average Bpm.

        Args:
            last_offset: If specified, this offset is used to
                terminate activity, else use the last note offset.

        Returns:
            ``float`` of average BPM.
        """
        last_offset = last_offset if last_offset else self.last_offset()
        sum_prod = np.sum(self.bpm * np.diff(self.offset, append=last_offset))
        return sum_prod / (last_offset - self.first_offset())
