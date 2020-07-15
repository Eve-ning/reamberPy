from __future__ import annotations

from dataclasses import dataclass
from reamber.bms.BMSNoteMeta import BMSNoteMeta

from reamber.base.Hit import Hit


@dataclass
class BMSHit(Hit, BMSNoteMeta):
    pass
