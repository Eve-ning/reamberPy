from __future__ import annotations

from typing import TypeVar

import numpy as np

from reamber.algorithms.timing import TimingMap, BpmChangeOffset
from reamber.base import Bpm
from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList

Item = TypeVar('Item')

@list_props(Bpm)
class BpmList(TimedList[Item]):
    """ A List that holds a list of Bpms, useful to do group Bpm operations """

    def current_bpm(self, offset: float, sort=True, delta=0.1):
        """ Finds the current BPM based on the offset provided

        :param offset: Offset to find associated bpm
        :param sort: Whether to sort the bpm implicitly. IT MUST BE SORTED!
        :param delta: A buffer for rounding errors
        :return: The associated Bpm Class.
        """
        bpms = self.sorted() if sort else self
        ix = int((np.sum((float(bpms.offset) - offset - delta) <= 0)) - 1)
        if ix < 0: raise IndexError(f"Offset {offset} does not have a Bpm Associated with it.")
        return bpms[ix]

    def reseat(self, item_cls: type):
        """ Because when we read the BMS file, sometimes the bpms aren't fitted properly, thus, we need to
        premptively reparse it by snapping to offset and back to snaps again.

        During _write_notes, if the time_by_offset tm isn't reparsed, corrective bpm lines will not generate.
        """
        tm = TimingMap.time_by_offset(self.first_offset(), [
            BpmChangeOffset(bpm=b.bpm, beats_per_measure=b.metronome, offset=b.offset) for b in self])

        return self.__class__([item_cls(b.offset, b.bpm, b.beats_per_measure) for b in tm.bpm_changes])

    def snap_offsets(self, nths: float = 1.0,
                     last_offset: float = None) -> np.ndarray:
        """ Gets all of the nth snap offsets

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

        :param nths: Specifies the beat's snap, 1 = "1st"s, 4 = "4th"s, 16 = "16th"s
        :param last_offset: The last offset to consider, if None, it uses the last BPM
        """
        self_ = self.deepcopy()
        if last_offset: self_ = self_.append(Bpm(last_offset, bpm=0))  # BPM doesn't matter for the last.

        offsets = []
        for i, j in zip(self_[:-1], self_[1:]):
            i: Bpm
            j: Bpm
            offset_diff = j.offset - i.offset
            nth_diff = i.beat_length / nths
            offsets.append(np.arange(0, offset_diff, nth_diff) + i.offset)
        return np.concatenate(offsets)

    def to_timing_map(self):
        return TimingMap.time_by_offset(
            initial_offset=self.first_offset(),
            bpm_changes_offset=[BpmChangeOffset(b.bpm, b.metronome, b.offset) for b in self]
        )

    def ave_bpm(self, last_offset: float = None) -> float:
        """ Calculates the average Bpm.

        :param last_offset: If not None, then this offset will be used to terminate activity,else last note offset will\
            be used.
        """
        last_offset = last_offset if last_offset else self.last_offset()
        sum_prod = np.sum(self.bpm * np.diff(self.offset, append=last_offset))
        return sum_prod / (last_offset - self.first_offset())
