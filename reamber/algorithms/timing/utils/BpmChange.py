from __future__ import annotations

from dataclasses import dataclass

from reamber.algorithms.timing.utils import BpmChangeOffset, BpmChangeSnap


@dataclass
class BpmChange(BpmChangeOffset, BpmChangeSnap):
    pass
