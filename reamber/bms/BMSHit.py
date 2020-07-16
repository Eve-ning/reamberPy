from __future__ import annotations

from dataclasses import dataclass

from reamber.base.Hit import Hit
from reamber.bms.BMSNoteMeta import BMSNoteMeta


@dataclass
class BMSHit(Hit, BMSNoteMeta):
    pass
