from dataclasses import dataclass
from typing import List

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap


@dataclass
class BpmChange:
    mspb: float
    metronome: float
    offset: float
    snap: Snap
    reseat_snap: Snap
    reseat_mspb: float

    @property
    def bpm(self):
        return 60000 / self.mspb

    @property
    def reseat_bpm(self):
        return 60000 / self.reseat_mspb

    @property
    def bpm_change_offset(self):
        return BpmChangeOffset(self.bpm, self.metronome, self.offset)

    @property
    def bpm_change_snap(self):
        return BpmChangeSnap(self.bpm, self.metronome, self.snap)

    @property
    def bpm_change_reseat_snap(self):
        return BpmChangeSnap(self.reseat_bpm, self.metronome, self.reseat_snap)

    @property
    def bpm_change_reseat_offset(self):
        return BpmChangeOffset(self.reseat_bpm, self.metronome, self.offset)


@dataclass
class Case:
    bpm_changes: List[BpmChange]

    @property
    def bpm_changes_offset(self):
        return [b.bpm_change_offset for b in self.bpm_changes]

    @property
    def bpm_changes_snap(self):
        return [b.bpm_change_snap for b in self.bpm_changes]

    @property
    def bpm_changes_reseat_snap(self):
        return [b.bpm_change_reseat_snap for b in self.bpm_changes]

    @property
    def bpm_changes_reseat_offset(self):
        return [b.bpm_change_reseat_offset for b in self.bpm_changes]
