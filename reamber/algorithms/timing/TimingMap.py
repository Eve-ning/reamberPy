from __future__ import annotations

from dataclasses import field, dataclass
from fractions import Fraction
from typing import List, Iterable, Tuple

import numpy as np
import pandas as pd

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.Snapper import Snapper
from reamber.algorithms.timing.utils.bpm_changes_offset_to_snap import \
    bpm_changes_offset_to_snap
from reamber.algorithms.timing.utils.from_bpm_changes_offset import \
    from_bpm_changes_offset
from reamber.algorithms.timing.utils.from_bpm_changes_snap import \
    from_bpm_changes_snap
from reamber.algorithms.timing.utils.reseat_bpm_changes_snap import \
    reseat_bpm_changes_snap
from reamber.algorithms.timing.utils.snap import Snap


@dataclass
class TimingMap:
    bpm_changes_offset: List[BpmChangeOffset] = \
        field(default_factory=lambda x: [])
    snapper: Snapper = Snapper()

    def bpm_changes_snap(self) -> List[BpmChangeSnap]:
        return bpm_changes_offset_to_snap(self.bpm_changes_offset,
                                          snapper=self.snapper)

    @staticmethod
    def from_bpm_changes_offset(
        bpm_changes_offset: List[BpmChangeOffset]
    ) -> TimingMap:
        return from_bpm_changes_offset(bpm_changes_offset)

    @staticmethod
    def from_bpm_changes_snap(
        initial_offset: float,
        bpm_changes_snap: List[BpmChangeSnap],
        reseat: bool = True
    ) -> TimingMap:
        return from_bpm_changes_snap(initial_offset, bpm_changes_snap, reseat)

    def reseat(self) -> TimingMap:
        return self.from_bpm_changes_snap(
            self.bpm_changes_offset[0].offset,
            self.bpm_changes_snap(),
            reseat=True
        )

    @staticmethod
    def reseat_bpm_changes_snap(
        bpm_changes_snap: List[BpmChangeSnap]
    ) -> List[BpmChangeSnap]:
        return reseat_bpm_changes_snap(bpm_changes_snap)

    def offsets(self, snaps: List[Snap]) -> np.ndarray:
        """Finds the offsets in ms for the specified snaps"""

        offsets: List[float] = []
        bc_i = -1
        snaps = np.array(snaps)
        sorter = snaps.argsort()
        bcs_s = self.bpm_changes_snap()

        for snap in reversed(snaps[sorter]):
            while bcs_s[bc_i].snap > snap:
                bc_i -= 1
            try:
                bcs = bcs_s[bc_i]
            except IndexError:
                raise IndexError("Failed to find BPM for snap.")

            diff_snap = snap - bcs.snap
            offsets.append(self.bpm_changes_offset[bc_i].offset +
                           diff_snap.offset(bcs))

        return np.array(offsets)[sorter[::-1].argsort()]

    def snaps(self, offsets: Iterable[float], snapper: Snapper) -> np.ndarray:
        """Finds the snaps from the provided offsets"""

        snaps: List[Snap] = []
        bc_i = -1
        bco_s = self.bpm_changes_offset
        bcs_s = self.bpm_changes_snap()
        offsets = np.array(offsets)
        sorter = offsets.argsort()
        for offset in reversed(offsets[sorter]):
            while self.bpm_changes_offset[bc_i].offset > offset:
                bc_i -= 1
            try:
                bco = bco_s[bc_i]
                bcs = bcs_s[bc_i]
            except IndexError:
                raise IndexError("Failed to find BPM for offset.")
            snaps.append(Snap.from_offset(offset, bco, bcs, snapper))

        return np.array(snaps)[sorter[::-1].argsort()]

    def beats(
        self, offsets: list[float], snapper: Snapper
    ) -> np.ndarray:
        """Finds the cumulative beats from the provided offsets"""

        if len(offsets) == 0: return np.asarray([])
        snaps = self.snaps(offsets, snapper)
        sorter = snaps.argsort()
        snaps_sort = snaps[sorter]
        curr_beat = snaps_sort[0].beat + \
                    Fraction(snaps_sort[0].measure) * \
                    Fraction(snaps_sort[0].metronome)
        beats = [curr_beat]
        for prev, curr in zip(snaps_sort[:-1], snaps_sort[1:]):
            diff = curr - prev
            curr_beat += Fraction(diff.measure * prev.metronome) + diff.beat
            beats.append(curr_beat)
        return np.array(beats)[sorter.argsort()]

    def get_active_bpm_by_offset(
        self, offset: float
    ) -> Tuple[BpmChangeOffset, BpmChangeSnap]:
        """Get the bpm affecting this offset"""
        # We loop in reverse to avoid having an upper limit offset check

        bcs_s = self.bpm_changes_snap()
        for bcs, bco in list(zip(bcs_s, self.bpm_changes_offset))[::-1]:
            if bco.offset > offset: continue
            return bco, bcs
        raise ValueError("Cannot find active BPM")

    def get_active_bpm_by_snap(
        self, snap: Snap
    ) -> Tuple[BpmChangeOffset, BpmChangeSnap]:
        """Get the bpm affecting this offset"""
        # We loop in reverse to avoid having an upper limit offset check

        bcs_s = self.bpm_changes_snap()
        for bcs, bco in list(zip(bcs_s, self.bpm_changes_offset))[::-1]:
            if bcs.snap > snap: continue
            return bco, bcs
        raise ValueError("Cannot find active BPM")

    def snap_objects(self,
                     offsets: Iterable[float],
                     objects: Iterable[object],
                     snapper: Snapper):
        # TODO: Deprecate this or smth
        a = pd.DataFrame([*self.snaps(offsets, snapper), objects]).T
        a.columns = ['measure', 'beat', 'slot', 'obj']
        a.measure = pd.to_numeric(a.measure)
        a.beat = pd.to_numeric(a.beat)

        return a
