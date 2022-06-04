from __future__ import annotations

from dataclasses import dataclass

from reamber.algorithms.timing.utils.BpmChangeBase import BpmChangeBase


@dataclass
class BpmChangeOffset(BpmChangeBase):
    offset: float
