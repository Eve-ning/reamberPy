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
        """Finds the current BPM of the offset

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

    def snap_offsets(self, nths: float = 1.0,
                     last_offset: float = None) -> np.ndarray:
        """Gets all of the nth snap offsets

        For example::

            SEC     1   2   3   4   5   6   7   8   9   10  11  12  13  14  ...
            BPM     15                          7.5                         ...
            SNAP    4/4 1/4 2/4 3/4 4/4 1/4 2/4 4/4 1/8 2/8 3/8 4/8 5/8 6/8 ...
            BEAT    1               2           3
            nths=1  ^               ^           ^
            nths=2  ^       ^       ^       ^   ^               ^
            nths=4  ^   ^   ^   ^   ^   ^   ^   ^       ^       ^       ^
            nths=8  ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^   ^   ^   ^   ^   ^   ^

        * Note: 15 BPM = 1 Beat per 4 seconds, 7.5 = 1 Beat per 8 seconds

        The `^` indicates what offsets will be returned.

        Args:
            nths: Specifies the beat's snap, 1 = "1st"s, 4 = "4th"s, 16 = "16th"s
            last_offset: The last offset to consider, if None, it uses the last BPM
        """
        bpm_list = self.deepcopy()

        # BPM doesn't matter for the last.
        if last_offset: bpm_list = bpm_list.append(Bpm(last_offset, bpm=0))

        offsets = []
        for i, j in zip(bpm_list[:-1], bpm_list[1:]):
            offset_diff = j.offset - i.offset
            nth_diff = i.beat_length / nths
            offsets.append(np.arange(0, offset_diff, nth_diff) + i.offset)
        return np.concatenate(offsets)

    def to_timing_map(self) -> TimingMap:
        return TimingMap.from_bpm_changes_offset(
            bpm_changes_offset=[
                BpmChangeOffset(b, m, o)
                for b, m, o in zip(self.bpm, self.metronome, self.offset)
            ]
        )

    def ave_bpm(self, last_offset: float = None) -> float:
        """Calculates the average Bpm.

        Args:
            last_offset: If specified, this offset is used to
                terminate activity, else use the last note offset.

        Returns:
            ``float`` of average BPM.
        """
        last_offset = last_offset if last_offset else self.last_offset()
        sum_prod = np.sum(self.bpm * np.diff(self.offset, append=last_offset))
        return sum_prod / (last_offset - self.first_offset())
