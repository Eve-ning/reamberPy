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

    @property
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
        bpm_changes_snap: List[BpmChangeSnap]
    ) -> TimingMap:
        return from_bpm_changes_snap(initial_offset, bpm_changes_snap)

    @staticmethod
    def reseat_bpm_changes_snap(
        bpm_changes_snap: List[BpmChangeSnap]
    ) -> List[BpmChangeSnap]:
        return reseat_bpm_changes_snap(bpm_changes_snap)

    def offsets(self, snaps: List[Snap]) -> np.ndarray:
        """ Finds the offsets in ms for the specified snaps """

        offsets: List[float] = []
        bc_i = -1
        snaps = np.array(snaps)
        sorter = snaps.argsort()

        for snap in reversed(snaps[sorter]):
            while self.bpm_changes_snap[bc_i].snap > snap:
                bc_i -= 1
            try:
                bcs = self.bpm_changes_snap[bc_i]
            except IndexError:
                raise IndexError("Failed to find BPM for snap.")

            diff_snap = snap - bcs.snap
            offsets.append(self.bpm_changes_offset[bc_i].offset +
                           diff_snap.offset(bcs))

        return np.array(offsets)[sorter.argsort()[::-1]]

    def snaps(self, offsets: Iterable[float], snapper: Snapper = Snapper()) \
        -> np.ndarray:
        """ Finds the snaps from the provided offsets """

        snaps: List[Snap] = []
        bc_i = -1
        offsets = np.array(offsets)
        sorter = offsets.argsort()
        for offset in reversed(offsets[sorter]):
            while self.bpm_changes_offset[bc_i].offset > offset:
                bc_i -= 1
            try:
                bco = self.bpm_changes_offset[bc_i]
            except IndexError:
                raise IndexError("Failed to find BPM for offset.")

            diff_offset = offset - bco.offset
            diff_snap = Snap.from_offset(diff_offset, bco, snapper)
            snaps.append(self.bpm_changes_snap[bc_i].snap + diff_snap)

        return np.array(snaps)[sorter.argsort()[::-1]]

    def beats(self, offsets: list[float], snapper: Snapper = Snapper()) \
        -> np.ndarray:
        """ Finds the cumulative beats from the provided offsets """

        if len(offsets) == 0: return np.asarray([])
        snaps = self.snaps(offsets, snapper)
        sorter = snaps.argsort()
        snaps = snaps[sorter]
        curr_beat = snaps[0].beat + \
                    snaps[0].measure * Fraction(snaps[0].metronome)
        beats = [curr_beat]
        for prev, curr in zip(snaps[:-1], snaps[1:]):
            diff = curr - prev
            curr_beat += Fraction(diff.measure * prev.metronome) + diff.beat
            beats.append(curr_beat)
        return np.array(beats)[sorter.argsort()]

    def get_active_bpm_by_offset(self, offset: float) \
        -> Tuple[BpmChangeOffset, BpmChangeSnap]:
        """ Get the bpm affecting this offset """
        # We loop in reverse to avoid having an upper limit offset check

        for bpm_active_snap, bpm_active_offset in \
            list(zip(self.bpm_changes_snap, self.bpm_changes_offset))[::-1]:
            if bpm_active_offset.offset > offset:
                continue

            return bpm_active_offset, bpm_active_snap
        raise ValueError("Cannot find active BPM")

    def get_active_bpm_by_snap(self, snap: Snap) \
        -> Tuple[BpmChangeOffset, BpmChangeSnap]:
        """ Get the bpm affecting this offset """
        # We loop in reverse to avoid having an upper limit offset check

        for bpm_active_snap, bpm_active_offset in \
            list(zip(self.bpm_changes_snap, self.bpm_changes_offset))[::-1]:
            if bpm_active_snap.snap > snap: continue

            return bpm_active_offset, bpm_active_snap
        raise ValueError("Cannot find active BPM")

    def snap_objects(self,
                     offsets: Iterable[float],
                     objects: Iterable[object],
                     snapper: Snapper = Snapper()):
        # TODO: Deprecate this or smth
        a = pd.DataFrame([*self.snaps(offsets, snapper), objects]).T
        a.columns = ['measure', 'beat', 'slot', 'obj']
        a.measure = pd.to_numeric(a.measure)
        a.beat = pd.to_numeric(a.beat)

        return a
