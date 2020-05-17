from __future__ import annotations
from reamber.base.BpmPoint import BpmPoint
from dataclasses import dataclass


@dataclass
class SMBpmPoint(BpmPoint):
    pass
    # beat: float = 0.0  # This must be calculated with offset.

