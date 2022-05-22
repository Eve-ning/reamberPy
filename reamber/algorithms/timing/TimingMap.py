from __future__ import annotations

from dataclasses import field, dataclass
from typing import List, Iterable, Tuple

import pandas as pd

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap
from reamber.algorithms.timing.utils.Snapper import Snapper


@dataclass
class TimingMap:
    initial_offset: float
    bpm_changes_offset: List[BpmChangeOffset] = \
        field(default_factory=lambda x: [])
    snapper: Snapper = Snapper()

    @property
    def bpm_changes_snap(self) -> List[BpmChangeSnap]:
        return ...

    def offsets(self, snaps: List[Snap]) -> List[float]:
        """ Finds the offsets in ms for the specified snaps """

        offsets = []

        for snap in sorted(snaps):
            bpm_active_offset, bpm_active_snap = \
                self.get_active_bpm_by_snap(snap)

            diff_snap = snap - bpm_active_snap.snap
            offsets.append(bpm_active_offset.offset +
                           diff_snap.offset(bpm_active_offset))

        return offsets

    def snaps(self, offsets: Iterable[float]) -> List[Snap]:
        """ Finds the snaps from the provided offsets """

        snaps: List[Snap] = []

        for offset in offsets:
            bpm_active_offset, bpm_active_snap = \
                self.get_active_bpm_by_offset(offset)

            diff_offset = offset - bpm_active_offset.offset
            diff_snap = Snap.from_offset(diff_offset, bpm_active_offset)
            snaps.append(bpm_active_snap.snap + diff_snap)

        return snaps

    def get_active_bpm_by_offset(self, offset: float) \
        -> Tuple[BpmChangeOffset, BpmChangeSnap]:
        """ Get the bpm affecting this offset """
        # We loop in reverse to avoid having an upper limit offset check

        for bpm_active_snap, bpm_active_offset in \
            list(zip(self.bpm_changes_snap, self.bpm_changes_offset))[::-1]:
            if bpm_active_offset.offset > offset: continue

            return bpm_active_offset, bpm_active_snap
        else:
            raise ValueError("Cannot find active BPM")

    def get_active_bpm_by_snap(self, snap: Snap) \
        -> Tuple[BpmChangeOffset, BpmChangeSnap]:
        """ Get the bpm affecting this offset """
        # We loop in reverse to avoid having an upper limit offset check

        for bpm_active_snap, bpm_active_offset in \
            list(zip(self.bpm_changes_snap, self.bpm_changes_offset))[::-1]:
            if bpm_active_snap.snap > snap: continue

            return bpm_active_offset, bpm_active_snap
        else:
            raise ValueError("Cannot find active BPM")

    def snap_objects(self,
                     offsets: Iterable[float],
                     objects: Iterable[object]):
        # TODO: Deprecate this or smth
        a = pd.DataFrame([*self.snaps(offsets), objects]).T
        a.columns = ['measure', 'beat', 'slot', 'obj']
        a.measure = pd.to_numeric(a.measure)
        a.beat = pd.to_numeric(a.beat)

        return a
