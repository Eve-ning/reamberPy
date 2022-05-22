from __future__ import annotations

from dataclasses import dataclass

from reamber.algorithms.timing.utils import BpmChangeBase, Snap


@dataclass
class BpmChangeSnap(BpmChangeBase):
    snap: Snap
